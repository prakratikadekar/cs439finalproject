import { useState } from 'react';

export default function Home() {
    const [query, setQuery] = useState("");

    const handleSearch = async() => {
        const response = await fetch("http://localhost:5000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({query}),
        
        });

        const results = await response.json();
        console.log(results);
    };

    return (
        <div className="flex flex-col items-center p-10">
            <h1 className='text-3x1 font-bold mb-6'>The Librarian</h1>

            <input
                className="border p-3 w-96 rounded"
                type="text"
                placeholder="What do you want to learn today?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />

            <button
                className='mt-4 bg-blue-600 text-white px-6 py-3 rounded'
            >
                Search
            </button> 
        </div>
    )
}