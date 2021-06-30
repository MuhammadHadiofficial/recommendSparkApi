from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))

# def decode_sentiment(score, include_neutral=True):
#     if include_neutral:        
#         label = NEUTRAL
#         if score <= SENTIMENT_THRESHOLDS[0]:
#             label = NEGATIVE
#         elif score >= SENTIMENT_THRESHOLDS[1]:
#             label = POSITIVE

#         return label
#     else:
#         return NEGATIVE if score < 0.5 else POSITIVE

# def predict(text, include_neutral=True):
#     start_at = time.time()
#     # Tokenize text
#     x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
#     print(x_test)
#     # # Predict
#     # score = model.predict([x_test])[0]
#     # # Decode sentiment
#     # label = decode_sentiment(score, include_neutral=include_neutral)

#     # return {"label": label, "score": float(score),
#     #    "elapsed_time": time.time()-start_at} 
