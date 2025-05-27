package com.datastudioasteroids.alma_paid_admin.repository

import com.datastudioasteroids.alma_paid_admin.data.dao.*
import com.datastudioasteroids.alma_paid_admin.network.ApiService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class DataRepository(
    private val api: ApiService,
    private val studentDao: StudentDao,
    private val courseDao: CourseDao,
    private val enrollmentDao: EnrollmentDao,
    private val invoiceDao: InvoiceDao
) {
    suspend fun fetchAndSyncAll() {
        val remote = api.fetchAll()
        withContext(Dispatchers.IO) {
            studentDao.upsertAll(remote.map { it.toStudent() })
            invoiceDao.upsertAll(remote.map { it.toInvoice() })
            // si agregas cursos/enrollments en el endpoint, haz lo mismo
        }
    }

    suspend fun markAsPaid(invoiceId: Long) {
        api.updateStatus(mapOf("id" to invoiceId.toString(), "status" to "PAID"))
        invoiceDao.updateStatus(invoiceId, "PAID")
    }

    fun getPendingInvoices() = invoiceDao.getByStatus("PENDING")
    fun getPaidInvoices() = invoiceDao.getByStatus("PAID")
}
