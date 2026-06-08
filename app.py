from generate import ask

def main():
    print("=" * 50)
    print("UofT CS Professor Review Bot")
    print("Ask me anything about CS professors at UofT")
    print("Type 'quit' to exit")
    print("=" * 50)

    while True:
        print()
        query = input("Your question: ").strip()
        if query.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        if not query:
            continue
        ask(query)

if __name__ == "__main__":
    main()