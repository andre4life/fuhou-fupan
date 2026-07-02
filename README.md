# 访后复盘引擎

## 在线地址
https://andre4life.github.io/fuhou-fupan/

## 维护说明

### 更新知识库索引
当保险知识库有新增/修改时，需要重新生成 kb-index.json：

```bash
cd C:\Users\18201\WorkBuddy\Claw\review-tool
python build-kb-index.py
```

然后将更新后的文件提交到 GitHub Pages：

```bash
cd D:\WorkBuddy输出\访后复盘引擎\output
cp C:\Users\18201\WorkBuddy\Claw\review-tool\public\kb-index.json .
git add -A
git commit -m "update: kb-index YYYY-MM-DD"
git push origin main
```

### 文件结构
- `index.html` — 主页面（复盘输入+分析+知识库参考）
- `admin.html` — 管理员后台（统计/搜索/删除/导入导出）
- `kb-index.json` — 知识库预索引（392篇）
- `build-kb-index.py` — 索引构建脚本
