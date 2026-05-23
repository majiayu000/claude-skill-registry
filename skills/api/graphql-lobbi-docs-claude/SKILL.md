---
name: graphql
description: GraphQL API development including schemas, resolvers, queries, mutations, and subscriptions. Activate for GraphQL servers, clients, and API design.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# GraphQL Skill

Provides comprehensive GraphQL development capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- GraphQL schema design
- Resolver implementation
- Query and mutation writing
- Subscriptions
- GraphQL client integration

## Schema Definition

\`\`\`graphql
# schema.graphql

type Query {
  agent(id: ID!): Agent
  agents(filter: AgentFilter, limit: Int = 10, offset: Int = 0): AgentConnection!
  task(id: ID!): Task
}

type Mutation {
  createAgent(input: CreateAgentInput!): Agent!
  updateAgent(id: ID!, input: UpdateAgentInput!): Agent!
  deleteAgent(id: ID!): Boolean!
  executeTask(input: ExecuteTaskInput!): Task!
}

type Subscription {
  agentStatusChanged(agentId: ID): Agent!
  taskCompleted(agentId: ID): Task!
}

type Agent {
  id: ID!
  name: String!
  type: AgentType!
  status: AgentStatus!
  config: JSON
  tasks(limit: Int = 10): [Task!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Task {
  id: ID!
  agent: Agent!
  message: String!
  result: String
  status: TaskStatus!
  createdAt: DateTime!
  completedAt: DateTime
}

type AgentConnection {
  edges: [AgentEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type AgentEdge {
  node: Agent!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

enum AgentType {
  CLAUDE
  GPT
  GEMINI
  OLLAMA
}

enum AgentStatus {
  IDLE
  ACTIVE
  ERROR
  OFFLINE
}

enum TaskStatus {
  PENDING
  RUNNING
  COMPLETED
  FAILED
}

input CreateAgentInput {
  name: String!
  type: AgentType!
  config: JSON
}

input UpdateAgentInput {
  name: String
  config: JSON
}

input ExecuteTaskInput {
  agentId: ID!
  message: String!
}

input AgentFilter {
  type: AgentType
  status: AgentStatus
  search: String
}

scalar DateTime
scalar JSON
\`\`\`

## Python Server (Strawberry)

\`\`\`python
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Agent:
    id: strawberry.ID
    name: str
    type: str
    status: str
    created_at: datetime

    @strawberry.field
    async def tasks(self, limit: int = 10) -> List["Task"]:
        return await task_service.get_by_agent(self.id, limit)

@strawberry.type
class Task:
    id: strawberry.ID
    message: str
    result: Optional[str]
    status: str
    created_at: datetime

@strawberry.input
class CreateAgentInput:
    name: str
    type: str
    config: Optional[strawberry.scalars.JSON] = None

@strawberry.type
class Query:
    @strawberry.field
    async def agent(self, id: strawberry.ID) -> Optional[Agent]:
        return await agent_service.get(id)

    @strawberry.field
    async def agents(
        self,
        type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Agent]:
        return await agent_service.list(type=type, status=status, limit=limit, offset=offset)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_agent(self, input: CreateAgentInput) -> Agent:
        return await agent_service.create(input)

    @strawberry.mutation
    async def delete_agent(self, id: strawberry.ID) -> bool:
        return await agent_service.delete(id)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def agent_status_changed(self, agent_id: Optional[strawberry.ID] = None) -> Agent:
        async for event in pubsub.subscribe("agent_status"):
            if agent_id is None or event.agent_id == agent_id:
                yield event

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

# FastAPI integration
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
\`\`\`

## Node.js Server (Apollo)

\`\`\`typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const typeDefs = `#graphql
  type Agent {
    id: ID!
    name: String!
    type: String!
    status: String!
  }

  type Query {
    agent(id: ID!): Agent
    agents: [Agent!]!
  }

  type Mutation {
    createAgent(name: String!, type: String!): Agent!
  }

  type Subscription {
    agentStatusChanged: Agent!
  }
`;

const resolvers = {
  Query: {
    agent: async (_, { id }, { dataSources }) => {
      return dataSources.agentAPI.getAgent(id);
    },
    agents: async (_, __, { dataSources }) => {
      return dataSources.agentAPI.getAllAgents();
    },
  },
  Mutation: {
    createAgent: async (_, { name, type }, { dataSources }) => {
      const agent = await dataSources.agentAPI.createAgent({ name, type });
      pubsub.publish('AGENT_CREATED', { agentCreated: agent });
      return agent;
    },
  },
  Subscription: {
    agentStatusChanged: {
      subscribe: () => pubsub.asyncIterator(['AGENT_STATUS_CHANGED']),
    },
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});
\`\`\`

## Client Queries

\`\`\`graphql
# Get single agent with tasks
query GetAgent($id: ID!) {
  agent(id: $id) {
    id
    name
    type
    status
    tasks(limit: 5) {
      id
      message
      status
      createdAt
    }
  }
}

# List agents with pagination
query ListAgents($type: AgentType, $limit: Int, $offset: Int) {
  agents(filter: { type: $type }, limit: $limit, offset: $offset) {
    edges {
      node {
        id
        name
        type
        status
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}

# Create agent
mutation CreateAgent($input: CreateAgentInput!) {
  createAgent(input: $input) {
    id
    name
    type
    status
  }
}

# Subscribe to status changes
subscription OnAgentStatusChanged($agentId: ID) {
  agentStatusChanged(agentId: $agentId) {
    id
    status
    updatedAt
  }
}
\`\`\`

## React Client (Apollo)

\`\`\`tsx
import { useQuery, useMutation, useSubscription, gql } from '@apollo/client';

const GET_AGENTS = gql`
  query GetAgents($type: AgentType) {
    agents(filter: { type: $type }) {
      edges {
        node {
          id
          name
          type
          status
        }
      }
    }
  }
`;

const CREATE_AGENT = gql`
  mutation CreateAgent($input: CreateAgentInput!) {
    createAgent(input: $input) {
      id
      name
    }
  }
`;

function AgentList() {
  const { loading, error, data } = useQuery(GET_AGENTS, {
    variables: { type: 'CLAUDE' }
  });

  const [createAgent] = useMutation(CREATE_AGENT, {
    refetchQueries: [GET_AGENTS]
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <ul>
      {data.agents.edges.map(({ node }) => (
        <li key={node.id}>{node.name}</li>
      ))}
    </ul>
  );
}
\`\`\`

## Best Practices

1. **Use Relay-style pagination** for lists
2. **Implement DataLoader** for N+1 prevention
3. **Add query complexity limits** for security
4. **Use input types** for mutations
5. **Version with field deprecation**, not URL versioning
6. **Document with descriptions** in schema
