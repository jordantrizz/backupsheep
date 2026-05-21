
# BackupSheep  
Automating backups is costly and takes time. With BackupSheep, you can quickly automate server snapshots and offsite backups - without writing code.  
 

## Databases (offsite backups):
Automate the backup process for your various databases like MySQL, PostgreSQL,  
MongoDB, and more. Our sophisticated retention policies enable you to retain any  
number of daily, weekly, or monthly backups as required.

 1. MySQL
 2. MariaDB
 3. PostgreSQL  

  
## Websites/Servers (offsite backups):  
Set up automatic backups of your files from any Linux-based operating system. With  
our sophisticated retention policies, you can maintain as many daily, weekly, or  
monthly backups as necessary.

 1. FTP
 2. FTPS
 3. sFTP
 4. SSH  

  
## Cloud Services (server snapshots):  
Automate periodic snapshots of your servers. Maintain any number of daily, weekly,  
or monthly backups you need with our rotation retention policies. We are compatible  
with all major cloud service providers.

 1. AWS
 2. DigitalOcean
 3. Google Cloud
 4. Hetzner
 5. Linode
 6. Oracle
 7. UpCloud
 8. Vultr

  
## SaaS Backups  (offsite backups):  
BackupSheep provides plugins and API integrations to secure your CMS and SaaS  
applications. This allows for the effortless safeguarding of your critical data.  
These tools are designed to seamlessly integrate with your existing systems,  
enabling easy and regular backups. Hence, you can rest easy knowing your valuable  
data is well-protected.

 1. Basecamp
 2. WordPress  
  
## Storage Integrations (for offsite backups):  
Connect your cloud storage providers and store backups in multiple storage accounts simultaneously.

 1. AWS S3
 2. Alibaba Cloud
 3. Azure
 4. BackBlaze B2
 5. Cloudflare R2
 6. DigitalOcean Spaces
 7. Dropbox
 8. ExoScale
 9. Filebase
 10. Google Cloud
 11. Google Drive
 12. IBM Cloud
 13. iDrive
 14. IONOS
 15. Levila
 16. Linode
 17. OneDrive
 18. Oracle
 19. pCloud
 20. RackCorp
 21. Scaleway
 22. Tencent
 23. UpCloud
 24. Vultr
 25. Wasabi  
  
## Notice  
This is a complete rewrite of the BackupSheep application. I have started pushing code to the repository,  but it is not functional yet. Please follow the repository to stay updated.  
  
## Technology Stack

Django, PostgreSQL, AlpineJS and TailwindCSS.

## Repository Map with Repomix

This repository can generate a repo map for high-level AI/code-review workflows using `repomix`.

Important: `.repomap-snapshot.md` can become extremely large, to the point of consuming millions of tokens. Treat it as a temporary, high-level artifact for extracting core features and repository structure, not as routine context to attach to every prompt.

In practice, this file should usually be generated once, used to help update high-level repository guidance such as `AGENTS.md`, and then left out of normal workflows. The snapshot is gitignored for that reason.

Install it globally if needed:

```bash
npm install -g repomix
```

Generate a lightweight repository snapshot with directory structure and metadata only:

```bash
repomix --no-files --style markdown --output .repomap-snapshot.md
```

Generate a richer structural map that compresses source files into high-level symbols such as classes and functions:

```bash
repomix --compress --style markdown --output .repomap-snapshot.md
```

Useful options for this repo:

- `--include-full-directory-structure` to force the full tree into the output.
- `--token-count-tree` to inspect which folders/files dominate the context window.
- `--no-git-sort-by-changes` if you want a stable alphabetical tree instead of git-weighted ordering.

If you explicitly need to refresh the repository summary, open `.repomap-snapshot.md`, extract the core structure and features you need, and fold that summary back into `AGENTS.md` instead of repeatedly sharing the full snapshot.

## Background

BackupSheep was a paid SaaS application from 2017 to 2023, serving over 6,500 users at its peak. Unfortunately, a poor decision to offer a lifetime deal (LTD) through AppSumo without proper due diligence led to a decline.
As a result, BackupSheep was shut down in 2023. Rather than letting years of development go to waste, I have decided to open source BackupSheep.
