import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="TextSum",
    page_icon="📝"
)

st.title("Text Summarizer")
st.subheader("Сервіс автоматичної сумаризації тексту")

st.write(
    "Вставте текст нижче і штучний інтелект "
    "створить його коротке резюме."
)

api_key = st.text_input(
    "Groq API Key",
    type="password"
)

text = st.text_area(
    "Введіть текст для сумаризації",
    height=250
)

if st.button("Створити резюме"):

    if not api_key:
        st.warning("Введіть API-ключ.")

    elif not text.strip():
        st.warning("Введіть текст для сумаризації.")

    else:
        try:
            client = Groq(api_key=api_key)

            with st.spinner("Створюю резюме..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Ти — помічник із сумаризації текстів. "
                                "Створи коротке резюме, зберігаючи "
                                "головні думки та факти. "
                                "Не додавай інформації від себе. "
                                "Поверни лише готове резюме "
                                "без вступів і привітань."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Підсумуй текст:\n\n{text}"
                        }
                    ],
                    temperature=0.2
                )

            result = response.choices[0].message.content

            st.subheader("Результат")
            st.write(result)

        except Exception as e:
            st.error(f"Помилка під час обробки: {e}")
