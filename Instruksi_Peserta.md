Siap, Riski. Kita buat instruksi **CloudWatch** menjadi bagian manual agar kamu bisa lebih memahami alurnya lewat klik-klik di konsol, sementara infrastruktur berat lainnya tetap kita "pukul" pakai **CloudFormation** (IaC).

Berikut adalah revisi final **Soal LKS Cloud Computing (v4.0)**. Soal ini sudah sangat mendalam, mencakup seluruh kisi-kisi, dan menggunakan **NAT Instance** sesuai preferensimu.

---

# Soal Lomba Kompetensi Siswa (LKS) - Cloud Computing (v4.0)
## Modul: Enterprise Infrastructure Automation & Hybrid-Cloud Storage

### Deskripsi Tugas
Perusahaan "CloudTech" sedang melakukan transformasi besar-besaran. Anda diminta untuk membangun infrastruktur yang otomatis namun tetap memiliki skalabilitas tinggi. Fokus utama adalah pada **High Availability**, **Shared Storage**, dan **Security**. Seluruh resource infrastruktur dasar wajib dibangun menggunakan **CloudFormation**, kecuali bagian pemantauan (*monitoring*) yang akan dikonfigurasi secara manual.

### Tujuan Utama yang harus diselesaikan:

#### 1. Networking & IaC (CloudFormation - Wajib)
Selesaikan template `infrastructure.yml` untuk membangun sumber daya berikut:
* **Networking (Multi-AZ):**
    * VPC dengan **2 Public Subnets** dan **2 Private Subnets** di dua Availability Zone berbeda.
    * Internet Gateway, Route Tables, dan Security Groups.
    * **NAT Instance:** Deploy 1 EC2 Instance (Amazon Linux 2023) di Public Subnet. Konfigurasikan agar instance ini berfungsi sebagai gateway internet bagi resource di Private Subnet.
* **Database & Storage:**
    * **Amazon RDS (MariaDB):** Deploy di Private Subnets dengan fitur Multi-AZ.
    * **Amazon DynamoDB:** Tabel `LKS-UserLogs` (Partition Key: `log_id`, Sort Key: `timestamp`).
    * **Amazon EFS:** Shared file system untuk Admin Panel, lengkap dengan *Mount Targets* di setiap AZ.
* **Storage & Messaging:**
    * **Amazon S3:** Bucket `cloudtech-assets-[nama-peserta]` lengkap dengan **Lifecycle Policy** (Otomatis pindah ke **Glacier** setelah 30 hari).
    * **Amazon SNS:** Topic `LKS-Registration-Alerts`.
* **Disaster Recovery:**
    * **AWS Backup:** Backup Vault (`lks-backup-vault`) dan Backup Plan harian untuk mencadangkan RDS, DynamoDB, dan EFS.

#### 2. Compute & High Availability (Elastic Beanstalk)
Deploy aplikasi Admin Panel dari folder `beanstalk_admin/`:
* **Environment:** Gunakan **Application Load Balancer (ALB)**.
* **Scaling:** Aktifkan **Auto Scaling Group** (Min: 2, Max: 4) berdasarkan penggunaan CPU.
* **Storage Integration:** Pastikan aplikasi Flask di Beanstalk dapat membaca/menulis ke **Amazon EFS** (Konfigurasi via `.ebextensions`).
* **OS:** Menggunakan **Amazon Linux 2023**.

#### 3. Serverless Workflow (API & Logic)
* **API Gateway:** Buat REST API `/users` (POST) yang terintegrasi dengan Step Functions.
* **Lambda Functions:**
    * `lks_post`: Menyimpan data ke MariaDB dan mengunggah foto profil (Base64) ke S3.
    * `lks_log_dynamo`: Mencatat metadata pendaftaran ke DynamoDB.
* **AWS Step Functions:** State Machine `LKS-Registration-Workflow` (Flow: Save RDS/S3 -> Log DynamoDB -> SNS Notify).

#### 4. Manual Configuration (Monitoring & Automation)
Lakukan konfigurasi berikut secara manual melalui AWS Console:
* **CloudWatch Dashboard:** Buat dashboard untuk memantau **CPU EC2** dan **RDS Connections**.
* **CloudWatch Alarm:** Buat alarm yang mengirim email via SNS jika CPU Beanstalk > 70%.
* **Amazon EventBridge:** Buat rule untuk mendeteksi status `FAILED` pada Step Functions dan mengirimkan alert ke SNS.

#### 5. Frontend & CI/CD
* **AWS Amplify:** Hubungkan GitHub repository.
* **Fitur:** Update form agar dapat mengirimkan **Nama**, **Email**, dan **File Foto** (convert ke Base64) ke API Gateway.

---

### Daftar Penamaan Resource (Case Sensitive):
| Resource | Nama Wajib |
| :--- | :--- |
| DynamoDB Table | `LKS-UserLogs` |
| SNS Topic | `LKS-Registration-Alerts` |
| Backup Vault | `lks-backup-vault` |
| S3 Bucket | `cloudtech-assets-[nama-peserta]` |
| Step Function | `LKS-Registration-Workflow` |
| RDS Database | `cloudtech_db` |

---

### Kriteria Penilaian Utama:
1.  **Automation:** Template CloudFormation berjalan tanpa error (Status: `CREATE_COMPLETE`).
2.  **Scalability:** Admin Panel dapat diakses via ALB URL dan memiliki minimal 2 instance berjalan.
3.  **End-to-End:** Pendaftaran dari web berhasil masuk ke RDS, fotonya masuk S3, dan log-nya masuk DynamoDB.
4.  **Resilience:** Notifikasi email masuk saat sistem sengaja dibuat gagal.

**Waktu Pengerjaan:** 5 Jam.
**Selamat Mendaftar LKS, Riski!**

---
