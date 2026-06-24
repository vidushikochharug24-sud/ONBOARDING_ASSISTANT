-- Workspaces (one per company domain)
CREATE TABLE workspaces (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  company_name TEXT NOT NULL,
  domain TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Users
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  workspace_id UUID REFERENCES workspaces(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Uploaded files (ZIPs and PDFs)
CREATE TABLE uploaded_files (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  file_path TEXT NOT NULL,
  original_name TEXT,
  file_type TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Generated onboarding guides
CREATE TABLE onboarding_guides (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  source_type TEXT NOT NULL,
  source_url TEXT,
  repo_name TEXT,
  guide_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Embedded code chunks for RAG chat
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE code_chunks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  guide_id UUID REFERENCES onboarding_guides(id) ON DELETE CASCADE,
  file_path TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(384) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX code_chunks_workspace_guide_idx ON code_chunks (workspace_id, guide_id);
CREATE INDEX code_chunks_embedding_idx ON code_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE OR REPLACE FUNCTION match_code_chunks(
  query_embedding VECTOR(384),
  match_workspace_id UUID,
  match_guide_id UUID,
  match_count INT DEFAULT 5
)
RETURNS TABLE (
  id UUID,
  workspace_id UUID,
  guide_id UUID,
  file_path TEXT,
  content TEXT,
  similarity FLOAT
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    code_chunks.id,
    code_chunks.workspace_id,
    code_chunks.guide_id,
    code_chunks.file_path,
    code_chunks.content,
    1 - (code_chunks.embedding <=> query_embedding) AS similarity
  FROM code_chunks
  WHERE code_chunks.workspace_id = match_workspace_id
    AND code_chunks.guide_id = match_guide_id
  ORDER BY code_chunks.embedding <=> query_embedding
  LIMIT match_count;
$$;
