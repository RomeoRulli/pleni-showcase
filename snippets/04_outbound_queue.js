// Sequential send queue of the WhatsApp gateway, with injected dependencies so it runs under `node --test`.
//
// Excerpt from `baileys-service/outbound_queue.js`. Comments and messages translated from Portuguese;
// code unchanged.
//
// It tells a 1-to-1 chat reply (fast, jumps the queue) from a batch send (long typing time plus jitter,
// to avoid a ban). An item that waits longer than `maxQueueWaitMs` is rejected with `queue_timeout` and
// is NEVER sent. That keeps the invariant "if the brain saw an error, the message did not go out".
// Before this, the brain's HTTP call timed out at 30 s, the brain retried on the next cycle, and the
// gateway still sent the old item: a duplicate reminder.

export const DEFAULT_MAX_QUEUE_WAIT_MS = 25000;
export const INTERACTIVE_WINDOW_MS = 60000;

export function queueTimeoutError(waitedMs) {
  const err = new Error(`queue_timeout: message waited ${Math.round(waitedMs / 1000)}s in the queue and was not sent`);
  err.code = 'queue_timeout';
  return err;
}

export class OutboundMessageQueue {
  /**
   * deps: isConnected(), resolveTargetJid(to), sendPresence(kind, jid), sendMessage(jid, content),
   *       delay(ms), lastInboundMs(phoneDigits), onSent(sent), logger, maskPhone,
   *       maxQueueWaitMs?, now?, setTimer?, clearTimer?, random?
   */
  constructor(deps) {
    this.deps = {
      maxQueueWaitMs: DEFAULT_MAX_QUEUE_WAIT_MS,
      now: Date.now,
      setTimer: setTimeout,
      clearTimer: clearTimeout,
      random: Math.random,
      maskPhone: (p) => String(p),
      onSent: () => {},
      ...deps
    };
    this.queue = [];
    this.processing = false;
    this.consecutiveSent = 0;
  }

  // `content` replaces the default `{ text }` (e.g. a contact card); `text` still sets the typing time.
  enqueue(to, text, interactive = false, content = null) {
    const { now, setTimer, clearTimer, maxQueueWaitMs } = this.deps;
    return new Promise((resolve, reject) => {
      const entry = { to, text, content, interactive: Boolean(interactive), queuedAt: now(), state: 'queued', timer: null };
      const settle = (fn, value) => {
        if (entry.timer) clearTimer(entry.timer);
        entry.state = 'done';
        fn(value);
      };
      entry.resolve = (value) => settle(resolve, value);
      entry.reject = (err) => settle(reject, err);
      // Cancel only while still queued: an item already being sent runs to the end and reports the real result.
      entry.timer = setTimer(() => {
        if (entry.state !== 'queued') return;
        entry.state = 'cancelled';
        const idx = this.queue.indexOf(entry);
        if (idx !== -1) this.queue.splice(idx, 1);
        this.deps.logger?.warn?.({ to: this.deps.maskPhone(to), waitedMs: maxQueueWaitMs }, 'Send cancelled: waited too long in the queue');
        reject(queueTimeoutError(maxQueueWaitMs));
      }, maxQueueWaitMs);

      if (entry.interactive) {
        // 1-to-1 chat replies jump ahead of batch sends (order among interactive items is kept)
        let idx = this.queue.findIndex((q) => !q.interactive);
        if (idx === -1) idx = this.queue.length;
        this.queue.splice(idx, 0, entry);
      } else {
        this.queue.push(entry);
      }
      this.processNext();
    });
  }
}
