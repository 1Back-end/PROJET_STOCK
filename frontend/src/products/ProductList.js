import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import axios from 'axios';
import Navbar from '../components/Navbar';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const perPage = 5;

  useEffect(() => {
    const fetchProducts = async () => {
      const token = JSON.parse(localStorage.getItem('token'));
      const accessToken = token ? token.access_token : null;

      if (!accessToken) {
        toast.error("Vous devez être connecté pour afficher les produits.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/get_all`, {
          headers: { Authorization: `Bearer ${accessToken}` },
          params: { page, per_page: perPage, order: 'desc', order_field: 'date_added' }
        });

        setProducts(response.data.data || []);
      } catch (error) {
        toast.error("Échec de la récupération des produits.");
      }
      setLoading(false);
    };

    fetchProducts();
  }, [page]);

  const handleDelete = async (productId) => {
    const token = JSON.parse(localStorage.getItem('token'));
    const accessToken = token ? token.access_token : null;

    if (!accessToken) {
      toast.error("Vous devez être connecté pour effectuer cette action.");
      return;
    }

    try {
      await axios.delete(`http://127.0.0.1:8000/api/v1/products`, {
        headers: { Authorization: `Bearer ${accessToken}` },
        data: { uuid: productId }
      });

      toast.success("Produit supprimé avec succès.");
      setProducts(products.filter(product => product.uuid !== productId));
    } catch (error) {
      toast.error("Échec de la suppression du produit.");
    }
  };

  return (
    <>
      <Navbar />
      <div className="container mt-4 py-5">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h3 className="text-brand">Liste des Produits</h3>
          <Link to="/add_product" className="btn btn-primary">+ Ajouter</Link>
        </div>

        {loading ? (
          <p>Chargement...</p>
        ) : (
          <div className="card-box p-3 shadow-sm">
            <table className="table table-striped table-bordered text-center">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Image</th>
                  <th>Produit</th>
                  <th>Catégorie</th>
                  <th>Quantité</th>
                  <th>Prix</th>
                  <th>Ajouté le</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {products.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="text-center">Aucun produit disponible.</td>
                  </tr>
                ) : (
                  products.map((product, index) => (
                    <tr key={product.uuid}>
                      <td>{(page - 1) * perPage + index + 1}</td>
                      <td>
                        <img 
                          src={product.avatar ? product.avatar.url : 'https://via.placeholder.com/50'}
                          alt={product.name} 
                          width="50" 
                          height="50" 
                        />
                      </td>
                      <td>{product.name}</td>
                      <td>{product.category ? product.category.name : 'Inconnue'}</td>
                      <td>{product.quantity}</td>
                      <td>{product.price} FCFA</td>
                      <td>{new Date(product.created_at).toLocaleString()}</td>
                      <td>
                      <Link to={`/product/${product.uuid}`} className="btn btn-info btn-sm text-white">Détails</Link>
                      <Link to={`/product/edit/${product.uuid}`} className="btn btn-warning text-white btn-sm mx-2">Modifier</Link>

                        <button className="btn btn-danger text-white btn-sm" onClick={() => handleDelete(product.uuid)}>Supprimer</button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}

        <div className="d-flex justify-content-center mt-4">
          <button 
            className="btn btn-secondary mr-2" 
            disabled={page === 1} 
            onClick={() => setPage(page - 1)}
          >
            Précédent
          </button>
          <span>Page {page}</span>
          <button 
            className="btn btn-secondary ml-2" 
            disabled={products.length < perPage} 
            onClick={() => setPage(page + 1)}
          >
            Suivant
          </button>
        </div>
      </div>
    </>
  );
};

export default ProductList;