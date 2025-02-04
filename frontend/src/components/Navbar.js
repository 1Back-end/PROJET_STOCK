import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTachometerAlt, faBoxes, faBoxOpen, faUsers, faTruck, faShoppingCart, faChartLine, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark text-white px-3 py-lg-3">
      <div className="container-fluid">
        {/* Logo */}

        <li className="nav-item text-decoration-none">
              <Link className="nav-link" to="/produits">
                <FontAwesomeIcon icon={faTachometerAlt} className="me-2" />
                Dashboard
              </Link>
            </li>

        {/* Bouton Toggle Mobile */}
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Menus */}
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/categories">
                <FontAwesomeIcon icon={faBoxes} className="me-2" />
                Catégories
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/produits">
                <FontAwesomeIcon icon={faBoxOpen} className="me-2" />
                Produits
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/clients">
                <FontAwesomeIcon icon={faUsers} className="me-2" />
                Clients
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/fournisseurs">
                <FontAwesomeIcon icon={faTruck} className="me-2" />
                Fournisseurs
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/commandes">
                <FontAwesomeIcon icon={faShoppingCart} className="me-2" />
                Commandes
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/ventes">
                <FontAwesomeIcon icon={faChartLine} className="me-2" />
                Ventes
              </Link>
            </li>
          </ul>

          {/* Bouton Logout */}
          <button className="btn btn-danger shadow-none btn-sm">
            <FontAwesomeIcon icon={faSignOutAlt} className="me-1" />
            Déconnexion
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
