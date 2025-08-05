#!/bin/bash

# GitHub 设置脚本
# 用于初始化 Git 仓库并上传到 GitHub

set -e

echo "🚀 开始设置 GitHub 仓库..."

# 检查是否已经初始化 Git
if [ ! -d ".git" ]; then
    echo "📁 初始化 Git 仓库..."
    git init
else
    echo "✅ Git 仓库已存在"
fi

# 添加所有文件
echo "📦 添加文件到 Git..."
git add .

# 检查是否有未提交的更改
if git diff --cached --quiet; then
    echo "ℹ️  没有新的更改需要提交"
else
    echo "💾 提交更改..."
    git commit -m "Initial commit: OCR text recognition server with GitHub Actions"
fi

# 提示用户输入 GitHub 仓库 URL
echo ""
echo "📝 请输入您的 GitHub 仓库 URL (例如: https://github.com/yourusername/text_recognition.git):"
read -r github_url

if [ -z "$github_url" ]; then
    echo "❌ 未提供 GitHub URL，退出"
    exit 1
fi

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin "$github_url" 2>/dev/null || git remote set-url origin "$github_url"

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git push -u origin main 2>/dev/null || git push -u origin master

echo ""
echo "✅ 设置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 访问您的 GitHub 仓库页面"
echo "2. 点击 'Actions' 标签页查看构建进度"
echo "3. 等待构建完成后下载构建产物"
echo ""
echo "📖 详细说明请查看: docs/GITHUB_ACTIONS_GUIDE.md" 