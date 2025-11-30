import {useState} from "react";

const Cards = ({item}) => (
    <div className="bg-white p-4 rounded-lg shadow-md mb-4 border-2" style={{borderColor: '#d7ba8e'}}>
        <h3 className="font-bold text-lg mb-2">
            {item.title || item}
        </h3>

        {
            item.author && (
                <p className="text-sm text-gray-600 mb-2">
                    By {item.author}
                </p>
            )
        }

        {
            item.description && (
                <p className="text-sm text-gray-700 mb-2">
                    {item.description}
                </p>
            )
        }

        {
            item.channel && (
                <p className="text-sm text-gray-600">
                    Channel: {item.channel}
                </p>
            )

            
        }

        { 
            item.url && (
                    <a 
                        href={item.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                    >
                        View Source
                    </a>
            )
        }
        
    </div>
);

const RecommedationColumn = ({title, items }) => (
    <div className="flex-1 min-w-0">
        <h2 className="text-2xl font-bold mb-4 pb-2 border-b-2" style={{borderColor: '#d7ba8e'}}> 
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
    const {books = [], articles = [], videos = []} = recommendations || {};
    
    return (
         <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8 flex justify-between items-center">
                    <div>
                        <h1>
                            Recommendation for: {query}
                        </h1>
                        
                        <p className="text-gray-600">
                            Here are books, articles, and videos based on what you want to learn.
                        </p>
                    </div>
                    <button onClick = {ToHomePage}
                    className="px-6 py-3 rounded-lg font-semibold transition-colors"
                    style={{backgroundColor: '#d7ba8e', color: 'white'}}
                        onMouseEnter = {(e) => {
                            if (query.trim()) {
                                e.target.style.backgroundColor = '#a1dffe';
                            } 
                        }}
                        onMouseLeave = {(e) => {
                            if (query.trim()) {
                                e.target.style.backgroundColor = '#d7ba8e';
                            }
                        }}
                    >
                        New Search
                    </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <RecommedationColumn title = "Books" items = {books} />
                    <RecommedationColumn title = "articles" items = {articles} />
                    <RecommedationColumn title = "Youtube Videos" items = {videos} />
                </div>
            </div>
        </div>
    );
}