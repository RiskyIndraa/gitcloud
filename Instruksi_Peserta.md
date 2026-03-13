# Soal Lomba Kompetensi Siswa (LKS) - Cloud Computing
## Modul: Modern Web Architectures & Serverless

### Deskripsi Tugas
Perusahaan "CloudTech" sedang bermigrasi ke arsitektur *Microservices & Serverless*. Anda ditugaskan sebagai Cloud Engineer untuk membangun infrastruktur di AWS dan memastikan aplikasi *front-end* ter-deploy dengan baik. Aplikasi ini akan menerima registrasi pengguna baru, yang prosesnya diatur menggunakan AWS Step Functions.

### Tujuan Utama yang harus diselesaikan:
1. **Frontend & CI/CD**: Deploy folder `amplify_frontend/` menggunakan AWS Amplify. Hubungkan repository Github lokal/remote Anda ke AWS Amplify untuk di-*hosting* otomatis.
2. **Infrastructure as Code (IaC)**: Selesaikan kode `infrastructure.yml` di folder `cloudformation/` untuk membangun:
   - VPC, Subnet, Route Table.
   - Amazon RDS (MariaDB) untuk database utama.
   - Amazon DynamoDB dengan nama tabel `LKS-UserLogs`.
3. **Fungsi Serverless**: Lengkapi script Python pada folder `lambda/` untuk:
   - Menyimpan *log* ke DynamoDB (menggunakan library `boto3`). 
   - (Catatan: Anda cukup menyesuaikan nama tabel dan *field* log-nya. Library `boto3` tidak perlu diinstal dalam `.zip` karena sudah *pre-installed* di AWS Lambda).
4. **AWS Step Functions (Workflow)**: Selesaikan definisi JSON di folder `step_functions/` untuk mengatur *workflow* registrasi:
   - Memanggil Lambda untuk simpan DB RDS.
   - Memanggil Lambda (yang telah Anda buat pada nomor 3) untuk mencatat log ke DynamoDB.
   - Mengirim notifikasi email via Amazon SNS.
5. **AWS Backup (Disaster Recovery)**:
   - Buat *Backup Plan* yang berjalan secara harian untuk mencadangkan data instance RDS dan tabel DynamoDB.
6. **Amazon EventBridge (Monitoring & Automation)**:
   - Buat sebuah *Rule* di EventBridge untuk memantau status eksekusi Step Functions yang gagal (*Failed*), dan rutekan targetnya agar memicu (trigger) peringatan ke Amazon SNS.
7. **AWS Elastic Beanstalk (Admin Panel)**:
   - Deploy aplikasi Flask (Python) yang ada pada folder `beanstalk_admin/` menggunakan **AWS Elastic Beanstalk** (koneksikan ke VPC yang sama jika diperlukan/diminta pada studi kasus).

### Direktori Kerja Peserta
- `/amplify_frontend` -> Source code front-end (HTML/JS) siap commit ke Github. Jangan ubah struktur jika tidak diperlukan, pastikan berjalan lancar di Amplify.
- `/cloudformation` -> Tempat Anda menuliskan template IaC (`infrastructure.yml`).
- `/lambda` -> Letakkan *source code* Python Lambda Anda di sini. Cukup siapkan `.py` (dan `requirements.txt` jika **benar-benar** butuh library eksternal, `boto3` sudah *built-in*).
- `/step_functions` -> Tempat *file* `registration_workflow.asl.json` yang akan mendefinisikan *State Machine*.
- `/beanstalk_admin` -> Source code aplikasi Admin (Flask/Python) untuk di-deploy ke AWS Elastic Beanstalk. File utama sudah disiapkan dengan nama `application.py`.

### Petunjuk Pengerjaan
1. Silakan mulai pengerjaan dari menyiapkan infrastruktur *networking* di file CloudFormation.
2. Buat repository Git, dan mulailah proses integrasi dengan AWS Amplify.
3. Kerjakan bagian logika Lambda dan pastikan Anda mengerti cara membaca datanya.
4. Buat dan *test* State Machine di layar konsol AWS dengan meng-copy kode JSON Anda.
5. Anda bebas melakukan iterasi (*trial & error*). 

**Waktu Pengerjaan:** 4 Jam
**Selamat Mengerjakan!**
