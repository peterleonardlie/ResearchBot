import media
import query as q

def search(data):
    query = q.QueryExtractor()
    try:
        if "news" in data.lower():
            # News Query
            query = query.get_news_tokens(data)
            response = media.Aggregator().get_news(query)
            if len(response) <= 0:
                return "Sorry, no relevant results were returned."
            i, done = 0, media.shorten_news(response[0])
            while (not done) and ((i + 1) < len(response)):
                i += 1
                done = shorten_news(response[i])
        else:
            # Knowledge Query
            done = media.get_gkg(query.get_knowledge_tokens(data))
        
        if not done:
            return "Sorry, no valid results were returned."
        
        return done
        
    except:
        return "Sorry, something unexpected happened."