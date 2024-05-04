import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import concurrent.futures

GOOGLE_API_KEY = "AIzaSyCOi5fgjuMr_T31Z2QfL0M2O3ZZXp_FzlU"  # Replace with your actual Google Generative AI API key
genai.configure(api_key=GOOGLE_API_KEY)

if "key_insights" not in st.session_state:
    st.session_state.key_insights = None

if "sentiment_scores" not in st.session_state:
    st.session_state.sentiment_scores = None

if "financial_performance" not in st.session_state:
    st.session_state.financial_performance = None

if "financial_position" not in st.session_state:
    st.session_state.financial_position = None

if "business_segments" not in st.session_state:
    st.session_state.business_segments = None

if "management_discussion" not in st.session_state:
    st.session_state.management_discussion = None

if "processed_company" not in st.session_state:
    st.session_state.processed_company = None


def get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    You are an experienced financial analyst with a deep understanding of financial statements and SEC filings. You will be provided 10K reports of a few companies:

Your Task:
Analyze the provided information to assess the company's overall financial health, performance, and potential for future growth. Pay close attention to revenue trends, profitability, debt levels, cash flow, and any significant financial risks or uncertainties.
Evaluate the company's competitive position within its industry. Consider its market share, competitive advantages, and any potential threats from competitors or market trends.
Based on your analysis, provide a clear and concise investment recommendation. Should investors consider buying this company's stock? Justify your recommendation by highlighting key factors influencing the company's future prospects and potential risks.
Remember, your analysis should be thorough, objective, and supported by evidence from the provided 10K sections.

    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the user asks your opinion, give your Opinions as an Expert Financial Analyst looking through all the documents, don't provide the wrong answer. If the user asks for sentiment analysis, analyze the documents carefully and provide a detailed sentiment analysis on them. While answering the questions try to use the name of the company while addressing it, instead of saying "The company". Please format your response using Markdown syntax for better readability. \n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0.3, google_api_key=GOOGLE_API_KEY)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question, chain, embeddings):
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    response = chain(
        {"input_documents": docs, "question": user_question}
        , return_only_outputs=True)

    return response["output_text"]


def delete_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")


def extract_analysis(text, chain, question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(text)

    response = chain(
        {"input_documents": docs,
         "context": text,
         "question": question}
        , return_only_outputs=True)

    return response["output_text"]


def process_pdf(pdf_path):
    text = get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(text)
    get_vector_store(text_chunks)
    return text


def main():
    st.set_page_config(page_title="AI Fin-Analyst", page_icon=":chart_with_upwards_trend:")
    st.title("AI Fin-Analyst 📈💰")

    selected_tab = st.sidebar.radio("Select Tab:", ["Sentiment & Key Insights", "User Queries"])

    if selected_tab == "Sentiment & Key Insights":
        st.sidebar.header("Options")
        selected_option = st.sidebar.selectbox("Select Company:", ["APPLE", "GOOGLE", "AMAZON"])

        if st.sidebar.button("Submit & Process"):
            with st.spinner("Processing..."):
                folder_mapping = {
                    "APPLE": "10k_filings/AAPL",
                    "GOOGLE": "10k_filings/GOOG",
                    "AMAZON": "10k_filings/AMZ"
                }

                selected_folder_path = folder_mapping.get(selected_option)

                if selected_folder_path:
                    pdf_files = []
                    if os.path.exists(selected_folder_path):
                        for file_name in os.listdir(selected_folder_path):
                            if file_name.endswith(".pdf"):
                                pdf_files.append(os.path.join(selected_folder_path, file_name))
                    else:
                        st.sidebar.warning("Invalid folder path.")

                    if pdf_files:
                        delete_existing_files("10k_filings")

                        with concurrent.futures.ProcessPoolExecutor() as executor:
                            processed_text = executor.map(process_pdf, pdf_files)

                        raw_text = '\n'.join(processed_text)
                        chain = get_conversational_chain()

                        for field in FIELDS:
                            st.session_state[field] = extract_analysis(raw_text, chain, get_field_question(field))
                        st.session_state.processed_company = selected_option

                        st.sidebar.success("Done")
                    else:
                        st.sidebar.warning("No PDF files found for the selected option.")
                else:
                    st.sidebar.warning("Please select a company.")

        for field in FIELDS:
            if st.session_state[field] is not None:
                st.header(get_field_title(field))
                with st.expander(f"See {get_field_title(field)}", expanded=False):
                    st.write(st.session_state[field])

    elif selected_tab == "User Queries":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
        st.write("Ask a Question from the PDF Files")
        user_question = st.text_input("", key="user_question")
        if user_question:
            chain = get_conversational_chain()
            user_response = user_input(user_question, chain, embeddings)  # Pass embeddings
            st.write("Reply:", user_response)


FIELDS = ["key_insights", "sentiment_scores", "financial_performance", "financial_position",
          "business_segments", "management_discussion"]


def get_field_question(field):
    questions = {
        "key_insights": "Summarize the key insights in 3-5 points that are relevant to investors and stockholders.",
        "sentiment_scores": "Analyze the sentiment of the overall 10k filings of the company and provide a detailed sentiment analysis.",
        "financial_performance": """Analyze the financial performance and trends of the company and state it in the following way: 
                                   Revenue Growth & Trends: Analyze the company's historical and current revenue growth, identifying key drivers and potential risks to future growth.
                                   Profitability: Assess the company's profitability through metrics like gross margin, operating margin, and net income. Evaluate trends and factors impacting profitability.
                                   Earnings per Share (EPS): Analyze EPS trends and compare them to industry peers to gauge the company's profitability on a per-share basis.
                                   Cash Flow: Examine the company's operating, investing, and financing cash flows to understand its liquidity, financial flexibility, and ability to generate cash..""",
        "financial_position": """Based on the reports, Assess the financial position and risk factors of the company. Debt Levels: Analyze the company's short-term and long-term debt, including debt-to-equity ratio and interest coverage ratio, to assess its financial leverage and risk.
                                 Liquidity: Evaluate the company's current ratio and quick ratio to understand its ability to meet short-term obligations.
                                 Working Capital Management: Assess the efficiency of managing current assets and liabilities, impacting the company's operational effectiveness.
                                 Contingencies & Commitments: Identify potential risks from lawsuits, guarantees, or other off-balance sheet obligations.""",
        "business_segments": """Evaluate the business segments and operations of the company. 
                                Segment Performance: Analyze the revenue, profitability, and growth trends of each business segment to understand the company's diversification and key drivers.
                                Competition: Assess the competitive landscape, including major competitors, market share, and potential threats from new entrants or substitutes.
                                Research & Development (R&D): Evaluate the company's R&D spending and its impact on innovation, product development, and future growth potential.""",
        "management_discussion": """Discuss the Management's Discussion and Analysis (MD&A) of the company. Management's Perspective: Gain insights into management's view of the company's performance, future outlook, and key risks and opportunities.
                                    Industry Trends & Challenges: Understand the broader industry context and how the company is positioned to navigate challenges and capitalize on trends.
                                    Strategic Initiatives: Analyze the company's strategic plans for growth, expansion, and value creation."""
    }
    return questions.get(field, "")


def get_field_title(field):
    titles = {
        "key_insights": "Key Insights:",
        "sentiment_scores": "Sentiment Analysis:",
        "financial_performance": "Financial Performance & Trends:",
        "financial_position": "Financial Position & Risk:",
        "business_segments": "Business Segments & Operations:",
        "management_discussion": "Management Discussion & Analysis (MD&A):"
    }
    return titles.get(field, "")


if __name__ == "__main__":
    main()
