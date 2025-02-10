import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import Navbar from '../components/Navbar';

const CategorieList = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);  // Page actuelle pour la pagination
  const [totalPages, setTotalPages] = useState(1);  // Nombre total de pages pour la pagination

  useEffect(() => {
    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;  // Extraire le access_token
    if (!accessToken) {
      toast.error('Veuillez vous connecter pour accéder à cette page');
      return;
    }

    const getAllCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/get_all', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
          params: {
            page: page,
            per_page: 10,
            order: 'desc',
            order_field: 'date_added',
          }
        });

        if (response.data.data.length === 0 && page > 1) {
          setPage(1);
        }
        
        setCategories(response.data.data); // Assure-toi d'utiliser `data` pour les catégories
        setTotalPages(response.data.total_pages); // Si tu veux gérer le total des pages
        setLoading(false);
      } catch (error) {
        if (error.response) {
          console.error('Détails de l\'erreur API:', error.response.data);
          if (error.response.data.detail === "dependencies-token-invalid") {
            toast.error('Token d\'authentification invalide. Veuillez vous reconnecter.');
          }
        } else {
          console.error('Erreur inconnue:', error.message);
        }
        toast.error('Échec de la récupération des catégories');
        setLoading(false);
      }
    };

    getAllCategories();
  }, [page]);

  const handleDelete = async (categoryId) => {
    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;
  
    if (!accessToken) {
      toast.error("Vous devez être connecté pour effectuer cette action.");
      return;
    }
  
    try {
      // Prépare les données à envoyer (ici, un objet avec le UUID de la catégorie)
      const data = { uuid: categoryId };
  
      const response = await axios.delete(`http://127.0.0.1:8000/api/v1/delete`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        data: data,  // Envoie le payload dans le corps de la requête
      });
  
      toast.success("Catégorie supprimée avec succès.");
      
      // Mettre à jour la liste des catégories après suppression
      setCategories(categories.filter(category => category.uuid !== categoryId));
  
    } catch (error) {
      toast.error("Erreur lors de la suppression:", error.response?.data || error.message);
      toast.error("Échec de la suppression de la catégorie.");
    }
  };
  

  return (
    <>
      <Navbar />
      <div className="container mt-4 py-5">
        {/* Titre + Bouton Ajouter */}
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3 className="text-brand">Liste des Catégories</h3>
          <Link to="/add_categorie" className="btn-add">
            + Ajouter
          </Link>
        </div>

        {/* Table des Catégories */}
        {loading ? (
          <p>Chargement...</p>
        ) : (
          <div className='card-box p-3 shadow-sm'>
            <table className="table table-striped table-bordered text-center">
              <thead>
                <tr>
                  <th>#</th> {/* Index */}
                  <th>Catégorie</th>
                  <th>Crée le</th>
                  <th>Ajouté par</th>
                  <th>Actions</th> {/* Colonne Actions */}
                </tr>
              </thead>
              <tbody>
                {categories.map((category, index) => (
                  <tr key={category.uuid}>
                    <td>{index + 1}</td> {/* Affichage de l'index */}
                    <td>{category.name}</td>
                    <td>{new Date(category.created_at).toLocaleString()}</td> {/* Date et heure */}
                    <td>{category.created_by.first_name} {category.created_by.last_name}</td>
                    <td>
                      {/* Bouton de suppression */}
                      <button
                        className="btn btn-danger btn-sm btn-xs"
                        onClick={() => handleDelete(category.uuid)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        <div className="d-flex justify-content-between mt-3">
          <button
            className="btn btn-outline-primary"
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            disabled={page === 1}
          >
            Précédent
          </button>
          <span>Page {page} sur {totalPages}</span> {/* Affiche aussi le total des pages */}
          {/* Afficher "Suivant" seulement si le total des pages est supérieur à 10 */}
          {totalPages > 10 && (
            <button
              className="btn btn-outline-primary"
              onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
              disabled={page === totalPages}
            >
              Suivant
            </button>
          )}
        </div>
      </div>
    </>
  );
};

export default CategorieList;
