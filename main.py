from app.agent import agent

question = "How is the current scene of affairs with the upcoming NEET re-examination conducted by NTA?"

result = agent.invoke({"question": question})

print("\n" + "=" * 60)
print("RESEARCH COMPLETE")
print("=" * 60)

print(f"\nQuestion: {result['question']}")
print(f"Iterations: {result['iterations']}")
print(f"Queries used: {len(result['queries'])}")

print("\nQueries:")
for i, q in enumerate(result["queries"], 1):
    print(f"  {i}. {q}")

print(f"\nSources gathered: {len(result['search_results'])}")

print("\n" + "-" * 60)
print("FINAL REPORT")
print("-" * 60)
print(result["final_response"])
print("=" * 60 + "\n")
