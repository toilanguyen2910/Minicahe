"""Minicahe Benchmark - evaluate token reduction and quality."""

import sys, os, difflib, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minicahe.compressor import compress_text
from minicahe.tokenizer import count_tokens, HAS_TIKTOKEN


SAMPLES = [
    {
        "name": "Email",
        "text": "Dear team, I am writing this email in order to provide you with an update regarding the current status of the project. Due to the fact that we have encountered some unexpected challenges, it is necessary that we postpone the deadline. At this point in time, we are in the process of conducting a thorough analysis of the situation, and I will make a decision about the next steps in the near future. In spite of these difficulties, I am able to confirm that we have made a significant amount of progress on the core functionality. A large number of the features have been completed, and we are now in the process of performing an assessment of the overall quality. Please take into consideration the fact that we need to provide support for the new requirements that came in. I would like to give an explanation for the delay during our next meeting. Best regards, John"
    },
    {
        "name": "ChatGPT",
        "text": "Thank you for your question! This is actually a really interesting topic, and I am happy to provide you with a comprehensive explanation. Basically, when it comes to understanding how machine learning models work, it is important to note that there are several key components that you should definitely take into consideration. First of all, a large number of the most popular models are based on the transformer architecture. In terms of how this architecture works, it essentially relies on a mechanism called self-attention, which allows the model to consider the relationship between different parts of the input. Having said that, it is worth mentioning that there are also some very important practical considerations when it comes to training these models. For example, you need to have a significant amount of high-quality training data, and you also need to make a decision about the appropriate model size. At the end of the day, the most important thing is to experiment and find what works best for your specific use case. I hope this explanation helps!"
    },
    {
        "name": "Technical",
        "text": "In the field of natural language processing, transformer-based models have become the dominant approach for a wide range of tasks. The architecture was first introduced in the paper Attention is All You Need by Vaswani et al. in 2017, and it has since revolutionized the way we approach sequence-to-sequence problems. The key innovation of the transformer architecture is the self-attention mechanism, which enables the model to capture long-range dependencies in the input sequence without the need for recurrent connections. This is achieved through the use of multi-head attention, where the model computes attention scores across multiple representation subspaces. When it comes to training these models, there are several important factors that need to be taken into consideration. These include the choice of optimizer, the learning rate schedule, the batch size, and the number of training steps. Additionally, the quality and quantity of the training data plays a crucial role in determining the final performance of the model. Despite these challenges, transformer-based models have achieved state-of-the-art results on a wide variety of NLP benchmarks, including machine translation, text summarization, question answering, and sentiment analysis. The success of these models can be attributed to their ability to scale effectively with increased compute and data."
    },
]

# placeholder
def calc_similarity(original, compressed):
    ow = original.lower().split()
    cw = compressed.lower().split()
    if not ow:
        return 1.0
        
    # Ignore stop words when calculating keyword preservation
    stop_words = {'that', 'this', 'have', 'from', 'they', 'with', 'what', 'were', 'been', 'some', 'very', 'just', 'really', 'actually', 'basically'}
    ok = set(w for w in re.findall(r'\b[a-z]{4,}\b', original.lower()) if w not in stop_words)
    ck = set(w for w in re.findall(r'\b[a-z]{4,}\b', compressed.lower()) if w not in stop_words)
    
    if not ok:
        return 0.0
    kw = len(ok & ck) / len(ok)
    matcher = difflib.SequenceMatcher(None, ow, cw)
    M = sum(triple.size for triple in matcher.get_matching_blocks())
    seq = M / len(cw) if len(cw) > 0 else 1.0
    return round(0.6 * kw + 0.4 * seq, 4)


def run():
    print("=" * 70)
    print("  MINICAHE BENCHMARK - GIAM TOKEN & CHAT LUONG")
    print("=" * 70)
    print("Tiktoken:", "OK" if HAS_TIKTOKEN else "FALLBACK")
    print()
    
    target_token, target_qual = 40, 90
    nr, ar = [], []
    
    for s in SAMPLES:
        n, t = s["name"], s["text"]
        ot = count_tokens(t)
        print(n)
        print("-" * 60)
        print("  Original: %d chars | %d tokens" % (len(t), ot))
        
        for m, mn in [(False, "NORMAL"), (True, "AGGRESSIVE")]:
            c = compress_text(t, aggressive=m)
            ct = count_tokens(c)
            sp = round((ot - ct) / ot * 100, 1) if ot > 0 else 0
            ql = round(calc_similarity(t, c) * 100, 1)
            tk = "OK" if sp >= target_token else "NO"
            qk = "OK" if ql >= target_qual else "NO"
            print("  [%9s] %4d tok | -%5.1f%% [%s] | CL: %5.1f%% [%s]" % (mn, ct, sp, tk, ql, qk))
            (ar if m else nr).append({"s": sp, "q": ql})
    
    print()
    print("=" * 70)
    print("  KET QUA TONG HOP")
    print("=" * 70)
    
    for lb, rs in [("NORMAL", nr), ("AGGRESSIVE", ar)]:
        a_s = sum(r["s"] for r in rs) / len(rs)
        a_q = sum(r["q"] for r in rs) / len(rs)
        p_s = sum(1 for r in rs if r["s"] >= target_token)
        p_q = sum(1 for r in rs if r["q"] >= target_qual)
        n = len(rs)
        st = "DAT MUC TIEU!" if (a_s >= target_token and a_q >= target_qual) else "CHUA DAT"
        print("  Mode %s:" % lb)
        print("    Giam token TB: %.1f%% (%d/%d dat %d%%)" % (a_s, p_s, n, target_token))
        print("    Chat luong TB: %.1f%% (%d/%d dat %d%%)" % (a_q, p_q, n, target_qual))
        print("    => %s" % st)
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    run()
