
---

# Soal Lomba Kompetensi Siswa (LKS) - Cloud Computing (v3.0)
## Modul: Enterprise Infrastructure Automation & Serverless Architecture

### Deskripsi Tugas
Perusahaan "CloudTech" memerlukan infrastruktur yang *robust*, *scalable*, dan sepenuhnya terdokumentasi dalam kode (IaC). Tugas Anda adalah membangun ekosistem pendaftaran user yang melibatkan penyimpanan aset, database relasional, log aktivitas, hingga panel admin yang memiliki ketersediaan tinggi (High Availability).

### Tujuan Utama yang harus diselesaikan:

#### 1. Infrastructure as Code (CloudFormation - Wajib)
Selesaikan template `infrastructure.yml` untuk membangun hampir seluruh sumber daya berikut secara otomatis:
* **Networking (Multi-AZ):** * VPC dengan 2 Public Subnets dan 2 Private Subnets di dua Availability Zone berbeda.
    * Internet Gateway dan Route Tables.
    * **NAT Instance:** Deploy 1 EC2 Instance (Amazon Linux 2023) di Public Subnet sebagai NAT Instance untuk memberikan akses internet ke Private Subnet (Konfigurasikan *Source/Dest Check* secara manual/script).
* **Database & Storage:**
    * **Amazon RDS (MariaDB):** Deploy di Private Subnets (Multi-AZ Deployment).
    * **Amazon DynamoDB:** Tabel `LKS-UserLogs` (Hash Key: `log_id`, Range Key: `timestamp`).
    * **Amazon EFS:** File system untuk *shared storage* Admin Panel, lengkap dengan *Mount Targets* di tiap AZ.
* **Storage & Messaging:**
    * **Amazon S3:** Bucket `cloudtech-assets-[nama-peserta]` dengan **Lifecycle Policy** (Move to Glacier after 30 days).
    * **Amazon SNS:** Topic `LKS-Registration-Alerts`.
* **Backup & Security:**
    * **AWS Backup:** Vault dan Plan harian untuk mencadangkan RDS, DynamoDB, dan EFS.
    * **Security Groups:** Aturan minimalis untuk akses antar layanan (Web, App, DB, EFS).

#### 2. Compute & High Availability (Elastic Beanstalk)
Deploy aplikasi Admin Panel dari folder `beanstalk_admin/`:
* **Platform:** Amazon Linux 2023 (Python 3.11/3.12).
* **Scaling:** Konfigurasikan **Application Load Balancer (ALB)** dan **Auto Scaling Group** (Min: 2, Max: 4) di dalam VPC.
* **EFS Integration:** Pastikan instance Beanstalk melakukan *mount* ke EFS yang dibuat di tahap 1 agar data admin tersinkronisasi.
* **Environment Properties:** Masukkan endpoint RDS, nama database, user, dan password sebagai variabel lingkungan.

#### 3. Serverless Logic (API Gateway, Lambda, Step Functions)
* **API Gateway:** Buat REST API dengan resource `/users` (Method POST).
* **AWS Lambda:** * `lks_post`: Simpan data user ke RDS dan upload foto profil (Base64) ke S3.
    * `lks_log_dynamo`: Catat aktivitas ke DynamoDB.
* **AWS Step Functions:** State Machine `LKS-Registration-Workflow` untuk mengatur urutan: `SaveToRDS&S3` -> `LogToDynamo` -> `SendSNSSuccess`.

#### 4. Monitoring & Proactive Alerts
* **CloudWatch Dashboard:** Buat dashboard visual untuk memantau:
    * CPU Utilization dari EC2 (Beanstalk Instances).
    * Database Connections dari RDS.
* **CloudWatch Alarm:** Kirim notifikasi ke SNS Topic jika CPU Utilization Beanstalk > 70%.
* **Amazon EventBridge:** Deteksi status `FAILED` pada Step Functions dan kirimkan alert ke SNS secara otomatis.

#### 5. Frontend & CI/CD
* **AWS Amplify:** Hubungkan ke repository GitHub Anda.
* **Feature:** Update form agar bisa menerima input **Nama, Email, dan Foto Profil** (dikirim sebagai Base64 JSON ke API Gateway).

---

### Detail Penamaan Resource (Wajib Sama):
| Resource | Nama / Nama Fisik |
| :--- | :--- |
| **DynamoDB Table** | `LKS-UserLogs` |
| **SNS Topic** | `LKS-Registration-Alerts` |
| **Backup Vault** | `lks-backup-vault` |
| **S3 Bucket** | `cloudtech-assets-[nama-peserta]` |
| **Step Function** | `LKS-Registration-Workflow` |
| **RDS DB Name** | `cloudtech_db` |

---

### Kriteria Kelulusan (Definition of Done):
1.  Frontend Amplify berhasil mengirim data dan foto profil.
2.  Step Function berjalan hijau (Succeeded).
3.  Admin Panel (Beanstalk) menampilkan data dari RDS dan bisa diakses via Load Balancer URL.
4.  Email notifikasi masuk ke inbox saat pendaftaran sukses atau Step Function sengaja dibuat gagal.
5.  Konfigurasi EFS terbukti aktif (shared file antar instance Beanstalk).

---

**Waktu Pengerjaan:** 5 Jam.
**Selamat Mengerjakan, Riski!**

---