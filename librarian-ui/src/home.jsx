import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";

export default function Home() {
    const [query, setQuery] = useState("");
    const navigate = useNavigate();

    const handleSubmit = () => {
        if (!query.trim()) return;
        navigate(`/results?query=${encodeURIComponent(query)}`);
    };


    // const handleSearch = async() => {
    //     const response = await fetch("http://localhost:5000/recommend", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json"},
    //         body: JSON.stringify({query}),
        
    //     });

    //     const results = await response.json();
    //     console.log(results);
    // };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-white px-4">
            <h1 className='text-3x1 font-bold mb-6'>What do you want to learn today?</h1>

            <p className="text-3xl font-semibold text-center mb-2">
                Type in a political or tech related topic and the Librarian will find the sources for you.
            </p>

            <SearchBar
                placeholder="I want to learn about..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onSubmit={handleSubmit}
            />

        </div>
    );
}

