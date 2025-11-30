import {useState} from "react";

const Cards = ({item}) => (
    <div>
        <h3>
            {item.title || item}
        </h3>

        {
            item.author && (
                <p>
                    By {item.author}
                </p>
            )
        }

        {
            item.description && (
                <p>
                    {item.description}
                </p>
            )
        }

        {
            item.channel && (
                <p>
                    Channel: {item.channel}
                </p>
            )
        }
    </div>
);

const RecommedationColumn = ({title, items, color }) => (
    <div>
        <h2>
            {title}
        </h2>
        {
            items.length > 0 ? (
                items.map((item, index) => (
                    <Cards key = {index} item = {item} />
                ))
            ) : (
                <p>
                    No {title.toLowerCase()} found in this query
                </p>
            )
        }
    </div>
);

export default function Recommend({recommendations, query, ToHomePage}) {
    const {books = [], articles = [], youtube = []} = recommendations || {};
    
    return (
        <div>
            <div>
                <div>
                    <div>
                        <h1>
                            Recommendation for: {query}
                        </h1>
                        
                        <p>
                            Here are books, articles, and videos based on what you want to learn.
                        </p>
                    </div>
                    <button onClick = {ToHomePage}
                        onMouseEnter = {(e) => {
                            if (!loading && query.trim()) {
                                e.target.style.backgroundColor = '#a1dffe';
                            }
                        }}
                        onMouseLeave = {(e) => {
                            if (!loading && query.trim()) {
                                e.target.style.backgroundColor = '#d7ba8e';
                            }
                        }}
                    >
                        New Search
                    </button>
                </div>
                <div>
                    <RecommedationColumn title = "Books" items = {books} />
                    <RecommedationColumn title = "articles" items = {articles} />
                    <RecommedationColumn title = "Youtube Videos" items = {youtube} />
                </div>
            </div>
        </div>
    );
}