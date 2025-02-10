import React, { useState } from 'react';
import Navbar from '../components/Navbar';  
import { toast } from 'react-toastify';  
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Categorie_Add = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!name) {
            toast.error("Veuillez renseigner le nom de la catégorie");
            return;
        }
        
        const token = JSON.parse(localStorage.getItem('token'));
        const accessToken = token ? token.access_token : null;
        if (!accessToken) {
            toast.error('Veuillez vous connecter pour accéder à cette page');
            return;
        }
        
        const CategorieData = { name};
        
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:8000/api/v1/create", CategorieData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            toast.success("Catégorie ajoutée avec succès");
            
            setTimeout(() => {
                setLoading(false);
                navigate('/categories');
            }, 1000);
        } catch (error) {
            setLoading(false);
            
            if (error.response?.data?.detail) {
                toast.error(error.response.data.detail);
            } else {
                toast.error('Erreur de connexion');
            }
            
        }
    };

    return (
        <div>
            <Navbar />
            <div className="container mt-5">
            <div className='col-md-6 col-sm-12'>
                <div className="card shadow-sm border-0 p-4">
                    <h1 className="mb-4 fw-bold" style={{ color: '#1F4283' }}>Ajouter une catégorie</h1>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="name" className="form-label">Nom de la catégorie</label>
                            <input type="text" className="form-control form-control-lg shadow-none" id="name" value={name} onChange={(e) => setName(e.target.value)} />
                        </div>
                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? 'Ajout en cours...' : 'Ajouter'}
                        </button>
                    </form>
                </div>
            </div>
            </div>
        </div>
    );
};

export default Categorie_Add;
