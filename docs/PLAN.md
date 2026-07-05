"""
Minicahe v2 - Kế hoạch cải thiện để đạt GIẢM 40-50% TOKEN, GIỮ 90% CHẤT LƯỢNG
================================================================================

Vấn đề hiện tại:
- Phrase map chỉ có ~50 cụm từ thông dụng
- Aggressive mode chỉ shorten ~15 từ đơn giản
- Không có xử lý cấp độ câu
- Không loại bỏ redundancy

Chiến lược cải thiện (3 phase):
"""

# ============================================================
# PHASE 1: MỞ RỘNG PHRASE MAP & FILLER (target: 20-25%)
# ============================================================

PHASE1_PHRASES = """
Thêm 200+ cụm từ verbose phổ biến:
  "a number of" → "some"
  "the majority of" → "most"  
  "are in agreement" → "agree"
  "has the capacity to" → "can"
  "in the process of" → "while"
  "on an ongoing basis" → "ongoing"
  "to the extent that" → "since"
  "is designed to provide" → "provides"
  "has been shown to be" → "is"
  ...
"""

PHASE1_FILLER = """
Thêm 100+ filler words và hedging language:
  "arguably" "presumably" "purportedly" "allegedly"
  "apparently" "seemingly" "supposedly" "ostensibly"
  "remarkably" "notably" "strikingly"
  ...
"""

# ============================================================
# PHASE 2: SENTENCE COMPRESSION (target: 30-40%)
# ============================================================

PHASE2_SENTENCE = """
Kỹ thuật nén cấp độ câu:
1. Loại bỏ mệnh đề quan hệ không cần thiết
   "The system, which is very important, ..." → "The system ..."
   
2. Rút gọn câu phức thành câu đơn
   "Because of the fact that X happened, Y occurred" → "X caused Y"

3. Loại bỏ giải thích/ví dụ dư thừa
   "For example, you might want to consider..." → (bỏ hoặc rút gọn)

4. Chuyển thể bị động → chủ động
   "It was decided by the team that..." → "The team decided..."
"""

# ============================================================
# PHASE 3: NLP-LIKE SUMMARIZATION (target: 40-50%) 
# ============================================================

PHASE3_NLP = """
Kỹ thuật nâng cao:
1. Key phrase extraction: Giữ lại danh từ/động từ chính (giống keywords)
2. Dependency-based trimming: Giữ subject-verb-object, bỏ modifier
3. Acronym injection: "machine learning" → "ML", "natural language processing" → "NLP"
4. Number normalization: "a large number of" → "many" → giữ số liệu cụ thể
5. List compression: "first, second, third" → "steps: 1) 2) 3)"
"""

# ============================================================
# IMPLEMENTATION ORDER
# ============================================================

ROADMAP = """
Tuần 1: Phase 1 - Mở rộng dictionary (ước tính: giảm 20-25%)
Tuần 2: Phase 2 - Sentence compression (ước tính: giảm 30-40%)  
Tuần 3: Phase 3 - NLP-like summarization (ước tính: giảm 40-50%)

Tổng: Cần mở rộng từ ~50 rules lên ~500+ rules + sentence-level processing
"""

if __name__ == "__main__":
    print("=" * 70)
    print("  MINICAHE v2 - KE HOACH CAI THIEN")
    print("=" * 70)
    print("""
  Trang thai hien tai: GIAM ~8-17% TOKEN (can 40-50%)
  
  >> CAN NANG CAP COMPRESSOR <=="")
    print(ROADMAP)
