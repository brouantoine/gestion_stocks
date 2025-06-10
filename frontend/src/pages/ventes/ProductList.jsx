import React from 'react';

const ProductList = ({ products, onRemove }) => {
  if (products.length === 0) return null;

  return (
    <div className="product-list">
      <h3>Détail de la transaction</h3>
      <table>
        <thead>
          <tr>
            <th>Produit</th>
            <th>Prix</th>
            <th>Qté</th>
            <th>Remise</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {products.map((item, index) => (
            <tr key={index}>
              <td>{item.product.designation}</td>
              <td>{item.unitPrice}€</td>
              <td>{item.quantity}</td>
              <td>{item.discount}%</td>
              <td>{(item.quantity * item.unitPrice * (1 - item.discount/100)).toFixed(2)}€</td>
              <td>
                <button onClick={() => onRemove(index)}>
                  ×
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductList;