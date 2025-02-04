import React, { useState } from 'react';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import loginImage from '../images/login.png'; // Importation de l'image

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!email) {
            toast.error('Veuillez renseigner votre email');
            return;
        }
        if (!password) {
            toast.error('Veuillez renseigner votre mot de passe');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                toast.success('Connexion réussie');
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('token', JSON.stringify(data.token));

                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 3000);
            } else {
                toast.error('Email ou mot de passe incorrect');
            }
        } catch (error) {
            toast.error('Erreur lors de la connexion');
            console.error(error);
        }
    };

    return (
        <div className="container min-vh-100 d-flex justify-content-center align-items-center border-5">
            <div className="row w-75 shadow-sm rounded-3 overflow-hidden">
                {/* Colonne de l'image */}
                <div className="col-md-6 d-flex justify-content-center align-items-center bg-light p-4">
                    <img src={loginImage} alt="Connexion" className="img-fluid rounded-circle" style={{ width: '80%', maxWidth: '300px' }} />
                </div>

                {/* Colonne du formulaire */}
                <div className="col-md-6 p-5 bg-white">
                    <h2 className="text-center mb-4" style={{ color: '#1F4283' }}>Connexion</h2>
                    <p className="text-center mb-4 text-muted">
                        Veuillez entrer vos informations de connexion pour accéder à votre compte
                    </p>

                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Email</label>
                            <input
                                type="email"
                                className="form-control form-control-lg"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="password" className="form-label">Mot de passe</label>
                            <input
                                type="password"
                                className="form-control form-control-lg"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <div className="d-flex justify-content-between mb-4">
                            <button type="submit" className="btn-primary btn-lg w-100 shadow-none">
                                Se connecter
                            </button>
                        </div>
                    </form>
                    <div className="text-center">
                        <a href="#" className="text-muted text-decoration-none">Mot de passe oublié ?</a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
