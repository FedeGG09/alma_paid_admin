package com.datastudioasteroids.alma_paid_admin.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.datastudioasteroids.alma_paid_admin.data.model.Invoice
import kotlinx.coroutines.flow.Flow

@Dao
interface InvoiceDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(list: List<Invoice>)

    @Query("SELECT * FROM invoices WHERE status = :status")
    fun getByStatus(status: String): Flow<List<Invoice>>

    @Query("UPDATE invoices SET status = :status WHERE id = :id")
    suspend fun updateStatus(id: Long, status: String)
}
