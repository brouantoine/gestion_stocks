import React from 'react';

const TypeSelector = ({ transactionType, setTransactionType, includeAllOption = false }) => (
  <div className="type-selector">
    {includeAllOption && (
      <label>
        <input
          type="radio"
          checked={transactionType === 'TOUS'}
          onChange={() => setTransactionType('TOUS')}
        />
        Tous types
      </label>
    )}
    <label>
      <input
        type="radio"
        checked={transactionType === 'VENTE_DIRECTE'}
        onChange={() => setTransactionType('VENTE_DIRECTE')}
      />
      Vente Directe
    </label>
    <label>
      <input
        type="radio"
        checked={transactionType === 'COMMANDE'}
        onChange={() => setTransactionType('COMMANDE')}
      />
      Commande Client
    </label>
  </div>
);

export default TypeSelector;