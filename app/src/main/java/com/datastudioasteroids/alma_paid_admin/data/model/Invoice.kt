package com.datastudioasteroids.alma_paid_admin.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "invoices")
data class Invoice(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val studentDni: String,
    val courseId: Long,
    val total: Double,
    val surcharge: Double,
    val status: String,
    val paidAt: Long? = null
)
