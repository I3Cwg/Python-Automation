from Whois_analyzer.analyzer import WhoisAnalyzer

if __name__ == "__main__":
    whois_analyzer = WhoisAnalyzer()
    domain = "example.com"
    result = whois_analyzer.query_domain(domain)
    print(result)