import {useState} from 'react';

export default function Home(ToRecommendationPage) {
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
                body: JSON.stringify({userQuery: userQuery.trim() }),
            });

            if (!response.ok) {
                throw new Error('Failed to get Recommedation');
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
        <div className="min-h-screen flex flex-col items-center justify-center bg-white px-4">
            <h1 className='text-3x1 font-bold mb-6'>What do you want to learn today?</h1>

            <p className="text-3xl font-semibold text-center mb-2">
                Type in a political or tech related topic and the Librarian will find the sources for you.
            </p>

            <div>
                <div>
                    <input type="text" value = {userQuery} onChange = {(e) => setUserQuery(e.target.value)} onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            handleSubmit(e);
                        }
                    }}
                    placeholder = "e.g, Clustering Algorithms, Government Shutdown"
                    disabled = {loading}
                    
                    onFocus = {(e) => e.target.style.borderColor = '#a1dffe'}
                    onBlur = {(e) => e.target.style.borderColor = '#d7ba8e'}
                    />
                    <button
                        onClick = {handleSubmit} disabled = {loading || !userQuery.trim()}
                        onMouseEnter = {(e) => {
                            if (!loading && userQuery.trim()) {
                                e.target.style.backgroundColor = '#a1dffe';
                            }
                        }}
                        onMouseLeave = {(e) => {
                            if (!loading && userQuery.trim()) {
                                e.target.style.backgroundColor = '#d7ba8e';
                            }
                        }}
                    >
                        {loading ? 'Looking For Recs' : 'Seach'}
                    </button>
                </div>
            </div>
        </div>
    );
}

