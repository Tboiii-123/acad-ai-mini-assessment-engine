from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re




def grade_text(question, submitted_answer):
    """
    Grades a text answer using:
    1. Exact match → full marks
    2. Keyword matching
    3. TF-IDF cosine similarity
    Returns marks between 0 and question.marks
    """

    max_marks = question.marks
    submitted_clean = submitted_answer.strip().lower()
    correct_clean = (question.correct_text_answer or "").strip().lower()

   
    if submitted_clean == correct_clean and submitted_clean:
        return max_marks

    keyword_score = 0
    if question.keywords:

        submitted_words = re.findall(r'\w+', submitted_clean)
        keywords = [k.lower() for k in question.keywords]

        matched = 0
        for k in keywords:
  
            if all(word in submitted_words for word in k.split()):
                matched += 1

        keyword_score = matched / len(keywords)

    # ---- 2. TF-IDF cosine similarity score ----
    cosine_score = 0
    if question.correct_text_answer:
        vectorizer = TfidfVectorizer(ngram_range=(1,2))
        tfidf_matrix = vectorizer.fit_transform([correct_clean, submitted_clean])
        cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


    combined_score = 0.5 * keyword_score + 0.5 * cosine_score
    awarded_marks = round(max_marks * combined_score)


    if submitted_clean and awarded_marks == 0:
        awarded_marks = 1

    return awarded_marks
