// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  // Importation des composants nécessaires pour le routage
import Login from './login/Login'; // Importation de la page de login
import { ToastContainer } from 'react-toastify'; // Importation de ToastContainer pour afficher les notifications Toast
import 'bootstrap/dist/css/bootstrap.min.css';  // Importation de Bootstrap pour le style de la page
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Importation de Bootstrap JS (pour le comportement interactif)
import './index.css';  // Importation du fichier CSS ici


// Importation des pages principales de l'application
import Dashboard from './dashboard/dashboard'; // Importation de la page Dashboard

import CategorieList from './categories/CategorieList';
import Categorie_Add from './categories/Categorie_Add';

function App() {
  return (
    <Router>
      <div>
        {/* Le composant Router permet de gérer la navigation entre les différentes pages */}

        {/* Définition des routes */}
        <Routes>
          {/* Route principale : page de login (affichée au démarrage) */}
          <Route path="/" element={<Login />} /> 

          {/* Route pour accéder à la page du dashboard */}
          <Route path="/dashboard" element={<Dashboard />} /> 

          {/* Route pour accéder à la liste des catégories */}
          <Route path="/categories" element={<CategorieList />} />

          {/* Route pour ajouter une nouvelle catégorie */}
          <Route path="/add_categorie" element={<Categorie_Add />} />
        </Routes>

        {/* Le composant ToastContainer permet d'afficher les notifications Toast (par exemple : succès, erreurs, etc.) */}
        <ToastContainer />
      </div>
    </Router>
  );
}

export default App;
