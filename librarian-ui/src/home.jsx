import {useState} from 'react';
import glasses from './assets/glasses-svgrepo-com.png';

export default function Home({ToRecommendationPage}) {
    const [userQuery, setUserQuery] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!userQuery.trim()) {
            return;
        }
 
        setLoading(true);

        try {
            // Send query to backend
            const response = await fetch('http://localhost:5000/api/recommend',{
                method:'POST', 
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify({query: userQuery.trim() }),
            });

            if (!response.ok) {
                throw new Error('Failed to get recommendations');
            }

            const data = await response.json();

            ToRecommendationPage(data, userQuery.trim());
        }

        catch (error) {
            console.error('Error:', error);
            alert('Failed to get recommendations. Please try again.');
        }

        finally {
            setLoading(false);
        }
    };


    return (
        <div className="home">
            <img src= {glasses} alt="Librarian Logo"/>

            <h1 className='title'>What do you want to learn today?</h1>

            <p className="librarian_description">
                Type in a political or tech related topic and the Librarian will find the sources for you.
            </p>

            <div className = "search_area">
                <div className = "search_box">
                    <input type="text" value = {userQuery} onChange = {(e) => setUserQuery(e.target.value)} onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            handleSubmit(e);
                        }
                    }}
                        placeholder = "e.g, Clustering Algorithms, Government Shutdown"
                        disabled = {loading}
                        className = "search_bar"
                    />
                    <button
                        onClick = {handleSubmit} disabled = {loading || !userQuery.trim()} className = "search_button"
                    >
                        {loading ? 'Looking For Recs' : 'Search'}
                    </button>
                </div>
            </div>
        </div>
    );
}

