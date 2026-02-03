To run this project locally, do these steps:

1.Clone the repository:

git clone https://github.com/<your-username>/LoopAi.git
cd LoopAi

2.Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate

3.Install dependencies:

pip install -r requirements.txt

4.Run the application
uvicorn server:app --reload


I have already uploaded the embedding vectors else you also have to run build_index.py.
