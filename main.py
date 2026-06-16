from langchain.messages import HumanMessage

from app.agent.graph import agent

question = "How does the Transformer architecture work?"

result = agent.invoke({"question":question})

print("\n" + "="*60)
print("RESEARCH COMPLETE")
print("="*60)

print(f"\nQuestion: {result['question']}")
print(f"Iterations: {result['iterations']}")
print(f"Queries used: {len(result['queries'])}")

print("\nQueries:")
for i, q in enumerate(result['queries'], 1):
    print(f"  {i}. {q}")

print(f"\nSources gathered: {len(result['search_results'])}")
for i, r in enumerate(result['search_results'], 1):
    print(f"  {i}. {r.get('title', 'No title')} — {r.get('url', 'No URL')}")

print("\n" + "-"*60)
print("FINAL REPORT")
print("-"*60)
print(result['final_response'])
print("="*60 + "\n")