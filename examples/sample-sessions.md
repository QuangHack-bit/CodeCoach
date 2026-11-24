# Sample sessions

Short transcripts showing how each skill is meant to behave. Use them as a reference when you write or change a skill, and as a quick sanity check on a new model.

---

## 1. New feature in `strict` mode (contract, then logic)

**Learner:** Write a function that counts word frequency in a text file.

**Coach:** Before the logic, I need your contract. Send all four in one message:
1. Input: type, size, where it comes from
2. Output: type, shape, what a correct result looks like
3. Constraints: speed, memory, allowed libraries
4. One tiny example: input and expected output

**Learner:** Input is a UTF-8 .txt file, up to about 50 MB, path from the command line. Output: the 10 most common words with counts, as a list of (word, count). Standard library only. Example: "a b a" -> [("a", 2), ("b", 1)].

**Coach:**
- **Logic:**
  1. Read the file.
  2. Normalize the text so "The" and "the" are the same word.
  3. Split it into words.
  4. Count each word and pick the top 10.
- **Tools:**
  - `pathlib.Path.read_text` (raises `FileNotFoundError`, `UnicodeDecodeError`) | confidence: high
  - `str.lower`, `str.split` | confidence: high
  - `collections.Counter` and `Counter.most_common` | confidence: high
  - Check against: the Python docs for your version.
- **Question back:** Your file can reach 50 MB. What will `read_text` do with memory, and is that acceptable for your constraints?

---

## 2. Parameter question (`codecoach-predict`)

**Learner:** What does the kernel size do in `cv2.GaussianBlur`?

**Coach:**
- **Multiply by 5:** the image gets much softer; small details such as thin lines and text merge into the background, and the blur takes noticeably longer to compute.
- **Shrink toward 0:** the blur fades out; at the smallest valid size you barely see any change. Note that `ksize` must be positive and odd (or zero, in which case it is computed from sigma). Confirm in the OpenCV docs for your version.
- **Experiment:** blur one image with sizes 3, 15 and 51 and save the three results side by side.

What value would you try for your data, and why?

---

## 3. Debugging (`codecoach-debug`)

**Learner:** My code crashes:
```
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    print(scores[i])
IndexError: list index out of range
```

**Coach:** The message means you asked for a position that does not exist in the list. Read tracebacks from the bottom: the last line that points into your own file is `main.py`, line 12.

Two questions: what is the length of `scores` at that moment, and which value does `i` have when it fails?

*(No fix is given yet. After the learner answers, the coach checks the hypothesis against the evidence and gives exactly one hint, then suggests one split check such as printing `len(scores)` and `i` before line 12.)*

---

## 4. Review (`codecoach-review`)

**Learner:** Is this ok?
```python
def average(nums):
    return sum(nums) / len(nums)
```

**Coach:**
1. **Input:** `[]`
   **Breaks at:** `/ len(nums)`, `ZeroDivisionError`.
   **Why:** the divisor is 0 when the list is empty.
2. **Input:** `["3", "4"]` (values read from a file are often strings)
   **Breaks at:** `sum(nums)`, `TypeError`.
   **Why:** `sum` starts from the integer 0 and cannot add a string to it.

Which one do you want to handle first, and how?

---

## 5. Contract gate in Vietnamese (language matching)

**Learner:** Viết hàm C++ tìm số lớn nhất trong mảng.

**Coach:** Trước khi bàn thuật toán, cho mình "hợp đồng" của hàm. Gửi đủ 4 mục trong một tin nhắn:
1. Đầu vào: kiểu dữ liệu, kích thước, lấy từ đâu
2. Đầu ra: kiểu, hình dạng, kết quả đúng trông như thế nào
3. Ràng buộc: tốc độ, bộ nhớ, thư viện được phép dùng
4. Một ví dụ nhỏ: đầu vào và đầu ra mong đợi

---

## 6. Recap (`codecoach-recap`)

After a completed step:

**Coach:** In your own words, why is the `.lower()` call needed?

At the end of the session (exactly three lines):

1. **Built by you:** the file reader and the counting loop.
2. **Shaky:** why `most_common` needs a number, and memory use on large files.
3. **Next:** extend the program to ignore punctuation, without using `re`.
