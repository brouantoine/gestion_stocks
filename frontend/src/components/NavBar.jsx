import React, { useState } from 'react';
import { Layout, Menu, Button, Dropdown, Avatar } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  ShoppingOutlined,
  UnorderedListOutlined,
  UserOutlined,
  LogoutOutlined,
  TeamOutlined,
  HomeOutlined
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

const NavBar = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
        Déconnexion
      </Menu.Item>
    </Menu>
  );

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        trigger={null}
        width={200}
        theme="light"
        style={{
          position: 'fixed',
          height: '100vh',
          zIndex: 1,
          boxShadow: '2px 0 8px 0 rgba(29,35,41,0.05)'
        }}
      >
        <div style={{ 
          padding: '16px', 
          textAlign: 'center',
          visibility: collapsed ? 'hidden' : 'visible'
        }}>
          <h2>Gestion Stock</h2>
        </div>
        
        <Menu
          mode="inline"
          theme="light"
          defaultSelectedKeys={['1']}
          style={{ borderRight: 0 }}
        >
          <Menu.Item key="1" icon={<HomeOutlined />}>
         <Link to="/">Dashboard</Link>
          </Menu.Item>
          <Menu.Item key="2" icon={<ShoppingOutlined />}>
            <Link to="/produits">Produits</Link>
          </Menu.Item>
          <Menu.Item key="3" icon={<UnorderedListOutlined />}>
            <Link to="/commandes">Commandes</Link>
          </Menu.Item>
          <Menu.Item key="4" icon={<TeamOutlined />}>
            <Link to="/clients">Clients</Link>
          </Menu.Item>
        </Menu>
      </Sider>

      <Layout style={{ 
        marginLeft: collapsed ? 80 : 200,
        transition: 'margin 0.2s'
      }}>
        <Header style={{ 
          padding: 0,
          background: '#fff',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingRight: 24
        }}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ width: 64, height: 64 }}
          />
          
          <Dropdown overlay={userMenu} placement="bottomRight">
            <div style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
              <Avatar icon={<UserOutlined />} />
              {!collapsed && <span style={{ marginLeft: 8 }}>Utilisateur</span>}
            </div>
          </Dropdown>
        </Header>

        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default NavBar;