// src/dashboard/dashboard.js
import React from 'react';
import Navbar from '../components/Navbar';  // Importation de la Navbar

const Dashboard = () => {
  return (
    <div>
      <Navbar />  {/* Afficher la Navbar */}
      
      {/* Le contenu du tableau de bord */}
      <div className="container mt-4">
        <h1>Bienvenue sur votre Tableau de bord</h1>
        {/* Ajoutez le reste du contenu ici */}
      </div>
    </div>
  );
};

export default Dashboard;
