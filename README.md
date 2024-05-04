# AI-Fin-analyst 📉💲

This is the repo of the AI Financial Analyst app, which is basically a Google Gemini 1.5 powered LLM RAG Application that provides Key Insights to users about Companies based on their 10K Report filings. For demonstration purposes, only the 5 latest 10K filings for each of the three companies are considered. Moreover, the app also provides users with the ability to chat with the documents and ask the LLM about any query regarding the 10K reports. 

**Note: The app takes some amount of time to process the documents. But once the documents are processed, the inference on them doesn't take much time at all. This is because loading the pdfs and cnverting into their vector forms take some time. I am trying to minimize this processing time in my next versions of the app**

**PS: The code for  Task1 (Downloading and Preprocessing the 10K files from SEC EDGAR) has been uploaded as an iPynb file named "SEC EDGAR 10K PReprocessing & Download**

**App Link:** https://ai-fin-analyst-b7qrhtxwisk5tdvsffvdor.streamlit.app/

## **App Structure**

<img width="249" alt="image" src="https://github.com/margamitra/AI-Fin-analyst/assets/72200003/7ed1c709-458a-4a0a-bf8a-57bfc18bd2f1">

Upon Starting the app, users are first greeted with a sidebar on the left where they can choose the company of their choice, and also whether they want to get the key insights and sentiment analysis of the company, or want to ask questions regarding the 10K filings.

On clicking the submit and process button after selecting the company, the 10K files for the companies are loaded and processed. The App then displays the "Key Insights" and various other Key Metrics and analysis of the company as follows: 

<img width="708" alt="image" src="https://github.com/margamitra/AI-Fin-analyst/assets/72200003/7d9d5828-f867-4c38-bcc8-3eba9940b1ff">

All the data are displayed under expandable text areas, which the user can then bring down and view, as per their choice. 

If the users want to ask any questions based on the reports, they can click on **User Queries** on the left sidebar and ask their queries in the chat area: 

<img width="709" alt="image" src="https://github.com/margamitra/AI-Fin-analyst/assets/72200003/a1c3af78-b3e8-4a9d-af0f-3453565fdd12">

## **Choice of Insights Being Displayed About a Company**

The Insights and data that are being displayed, based on the analysis of the 10K filings, are as follows: 

<img width="791" alt="image" src="https://github.com/margamitra/AI-Fin-analyst/assets/72200003/b894a752-c34e-4fea-b080-85c7a5629d87">

The insights highlighted are crucial for investors because they provide a comprehensive understanding of a company's financial health, performance, and future prospects. Here's why each area is significant:

**1. Financial Performance & Trends:**
   - **Predicting Future Performance:** Understanding historical and current financial performance helps investors predict future earnings, cash flows, and growth potential.
   - **Evaluating Management Effectiveness:** Analyzing trends in revenue, profitability, and EPS reveals how effectively management utilizes resources and generates returns.
   - **Assessing Investment Risk:** Financial performance metrics like debt levels and cash flow help evaluate the company's financial risk and ability to withstand economic downturns.

**2. Financial Position & Risk:**
   - **Gauging Financial Stability:** Analyzing debt, liquidity, and working capital management reveals the company's financial stability and ability to meet its obligations.
   - **Understanding Financial Leverage:** Assessing debt levels helps investors understand the company's financial risk and its potential impact on earnings and cash flow.
   - **Identifying Potential Threats:** Contingencies and commitments can pose significant financial risks, and investors need to be aware of their potential impact.

**3. Business Segments & Operations:**
   - **Evaluating Diversification:** Understanding the performance of different business segments helps investors assess the company's diversification and its impact on risk and growth.
   - **Assessing Competitive Advantage:** Analyzing the competitive landscape reveals the company's strengths and weaknesses relative to its peers and potential threats to its market position.
   - **Understanding Innovation & Growth Potential:** R&D spending is an indicator of the company's commitment to innovation and its potential for future growth.

**4. Management Discussion & Analysis (MD&A):**
   - **Gaining Management's Perspective:** MD&A provides valuable insights into management's strategy, outlook, and assessment of key risks and opportunities.
   - **Understanding Industry Dynamics:** MD&A often discusses industry trends, challenges, and the company's competitive positioning within the industry.
   - **Assessing Future Plans:** MD&A reveals the company's strategic initiatives and plans for future growth and value creation.

The "Key insights" provide users with the overall overview of the company's performance based on the analysis of all the filed 10K records, and the "Sentiment Analysis" performs an overall sentiment analysis of the text in the reports. 

## **Choice of Tech Stack**

This app analyzes the 10K filings of the companies and provides valuable insights on them. Additionally, it is also made into a RAG application so that users can chat with the documents with the help of the LLM API. The choice of tech stacks used in the development of this app are:

1. **Streamlit:**
    - **Rationale:** Streamlit is a Python library that simplifies the creation of interactive web applications, making it easy to build user interfaces.

2. **PyPDF2:**
    - **Rationale:** PyPDF2 is a Python library used for extracting text and metadata from PDF files, which is essential for processing the 10K reports and converting them into a format suitable for analysis.

3. **LangChain:**
    - **Rationale:** LangChain is a framework designed to simplify the development of applications powered by large language models (LLMs). It provides tools for text splitting, embedding, vector stores, and chain creation, streamlining the process of building a RAG application.

4. **Google Generative AI (GenAI):**
    - **Rationale:** GenAI offers powerful LLMs and embedding models that are used for understanding and generating text, forming the core of the question-answering and insight extraction capabilities of the application.

5. **FAISS:**
    - **Rationale:** FAISS is an efficient library for similarity search, enabling the application to find relevant sections of the 10K report that are most likely to contain answers to user queries or insights related to specific aspects of the company's financials.

6. **Concurrent.Futures:**
    - **Rationale:** This Python module enables parallel processing, allowing the application to extract text and process PDFs concurrently, thereby significantly reducing the overall processing time.
  


