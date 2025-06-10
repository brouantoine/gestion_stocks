import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Typography, theme } from 'antd';
import { 
  ShoppingOutlined, 
  UnorderedListOutlined,
  UserOutlined,
  PieChartOutlined,
  DollarOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { useToken } = theme;

const Dashboard = () => {
  const { token } = useToken();
  const navigate = useNavigate();

  const dashboardItems = [
        { 
      title: 'Ventes', 
      icon: <DollarOutlined style={{ fontSize: '32px' }} />,
      path: '/ventecommande',
      color: token.colorProcessing,
      description: 'Tableau des ventes'
    },
    { 
      title: 'Produits', 
      icon: <ShoppingOutlined style={{ fontSize: '32px' }} />,
      path: '/produits',
      color: token.colorPrimary,
      description: 'Gestion du catalogue produits'
    },
    
    { 
      title: 'Commandes', 
      icon: <UnorderedListOutlined style={{ fontSize: '32px' }} />,
      path: '/commandes',
      color: token.colorSuccess,
      description: 'Voir toutes les commandes'
    },
    { 
      title: 'Clients', 
      icon: <UserOutlined style={{ fontSize: '32px' }} />,
      path: '/clients',
      color: token.colorWarning,
      description: 'Gestion des clients'
    },
    { 
      title: 'Statistiques', 
      icon: <PieChartOutlined style={{ fontSize: '32px' }} />,
      path: '/statistiques',
      color: token.colorInfo,
      description: 'Analytiques des ventes'
    },
    { 
      title: 'Utilisateurs', 
      icon: <UserOutlined style={{ fontSize: '32px' }} />,
      path: '/utilisateurs',
      color: token.colorProcessing,
      description: 'Liste des utilisateurs'
    }
  ];
  return (
    <div style={{ 
      padding: '24px', 
      maxWidth: '1400px', 
      margin: '0 auto',
      backgroundColor: token.colorBgContainer
    }}>
      <Title level={2} style={{ marginBottom: '24px' }}>Tableau de Bord</Title>
      
      <Row gutter={[24, 24]}>
        {dashboardItems.map((item, index) => (
          <Col key={index} xs={24} sm={12} md={8} lg={8} xl={6}>
            <Card 
              hoverable
              onClick={() => navigate(item.path)}
              style={{ 
                height: '220px',
                borderRadius: '12px',
                border: `1px solid ${token.colorBorderSecondary}`,
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
                transition: 'all 0.3s ease',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center'
              }}
              bodyStyle={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '24px'
              }}
            >
              <div style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                backgroundColor: `${item.color}10`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '16px'
              }}>
                {React.cloneElement(item.icon, { 
                  style: { 
                    color: item.color,
                    fontSize: '24px'
                  } 
                })}
              </div>
              <Title level={4} style={{ marginBottom: '8px' }}>{item.title}</Title>
              <Text type="secondary" style={{ textAlign: 'center' }}>{item.description}</Text>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default Dashboard;