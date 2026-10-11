#!/bin/bash
cd "$(dirname "$0")/frontend"
npm ci
npm run dev
