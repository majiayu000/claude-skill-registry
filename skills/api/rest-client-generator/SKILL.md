---
name: rest-client-generator
description: Generate REST API client code in multiple languages with error handling. Use when creating API client libraries or SDK code.
---

# REST Client Generator Skill

REST API クライアントコードを生成するスキルです。

## 主な機能

- **Axios クライアント**: JavaScript/TypeScript
- **Fetch API**: モダンJavaScript
- **Requests**: Python
- **HTTPClient**: Java

## Axios (TypeScript)

```typescript
import axios, { AxiosInstance } from 'axios';

class UserAPI {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      }
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
        }
        return Promise.reject(error);
      }
    );
  }

  async getUsers(): Promise<User[]> {
    const { data } = await this.client.get('/users');
    return data;
  }

  async createUser(user: CreateUserDTO): Promise<User> {
    const { data } = await this.client.post('/users', user);
    return data;
  }

  async updateUser(id: string, user: UpdateUserDTO): Promise<User> {
    const { data } = await this.client.put(`/users/${id}`, user);
    return data;
  }

  async deleteUser(id: string): Promise<void> {
    await this.client.delete(`/users/${id}`);
  }
}

export const userAPI = new UserAPI('https://api.example.com');
```

## Python (requests)

```python
import requests
from typing import List, Optional

class UserAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def get_users(self) -> List[dict]:
        response = self.session.get(f'{self.base_url}/users')
        response.raise_for_status()
        return response.json()

    def create_user(self, user_data: dict) -> dict:
        response = self.session.post(
            f'{self.base_url}/users',
            json=user_data
        )
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: str, user_data: dict) -> dict:
        response = self.session.put(
            f'{self.base_url}/users/{user_id}',
            json=user_data
        )
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: str) -> None:
        response = self.session.delete(f'{self.base_url}/users/{user_id}')
        response.raise_for_status()
```

## バージョン情報
- Version: 1.0.0
