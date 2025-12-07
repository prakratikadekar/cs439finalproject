const Cards = ({item}) => (
    <div className = {`recommendation_card ${item.url ? 'has_link' : ''}`} onClick ={() => {
        if (item.url) window.open(item.url, '_blank');
    }}>
        <h3 className="each_card_title">
            {item.title || item}
        </h3>

        {
            item.author && (
                <p className="each_card_part">
                    By {item.author}
                </p>
            )
        }

        {
            item.description && (
                <p className="each_card_part">
                    {item.description}
                </p>
            )
        }

        {
            item.channel && (
                <p className="each_card_part">
                    Channel: {item.channel}
                </p>
            )

            
        }

        {
            (item.isbn10 || item.isbn13) && (
                <div>
                    {
                        item.isbn10 && (
                            <p className = "each_card_part">ISBN-10: {item.isbn10}</p>
                        )
                    }
                    {
                        item.isbn13 && (
                            <p className = "each_card_part">ISBN-13: {item.isbn13}</p>
                        )
                    }
                </div>
            )
        }
    </div>
);

const RecommendationColumn = ({title, items }) => (
    <div className="each_column">
        <h2 className="column_title"> 
            {title}
        </h2>
        {
            items.length > 0 ? (
                items.map((item, index) => (
                    <Cards key = {index} item = {item} />
                ))
            ) : (
                <p className="each_card_part">
                    No {title.toLowerCase()} found in this query
                </p>
            )
        }
    </div>
);

export default function Recommend({recommendations, query, ToHomePage}) {
    const {books = [], articles = [], videos = []} = recommendations || {};
    
    return (
        <div className="recommendation">
            <div className="recommendation_box">
                <div className="recommendation_inner_box">
                    <div>
                        <h1 className = "recommendation_title">
                            Recommendation for: {query}
                        </h1>
                        
                        <p className="recommendation_description">
                            Here are books, articles, and videos based on what you want to learn.
                        </p>
                    </div>

                    <button onClick = {ToHomePage} className="new_search_button">
                        New Search
                    </button>
                </div>

                <div className="column">
                    <RecommendationColumn title = "Books" items = {books} />
                    <RecommendationColumn title = "Articles" items = {articles} />
                    <RecommendationColumn title = "Youtube Videos" items = {videos} />
                </div>
            </div>
        </div>
    );
}