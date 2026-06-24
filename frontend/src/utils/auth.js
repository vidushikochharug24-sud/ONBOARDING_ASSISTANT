export const getToken = () => localStorage.getItem('token');

export const setToken = (token) => localStorage.setItem('token', token);

export const removeToken = () => localStorage.removeItem('token');

export const isAuthenticated = () => !!getToken();

export const getUserEmail = () => localStorage.getItem('email');

export const setUserEmail = (email) => localStorage.setItem('email', email);

export const getCompanyName = () => localStorage.getItem('company_name');

export const setCompanyName = (company_name) => localStorage.setItem('company_name', company_name);

export const getWorkspaceId = () => localStorage.getItem('workspace_id');

export const setWorkspaceId = (workspace_id) => localStorage.setItem('workspace_id', workspace_id);

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('email');
  localStorage.removeItem('company_name');
  localStorage.removeItem('workspace_id');
};
