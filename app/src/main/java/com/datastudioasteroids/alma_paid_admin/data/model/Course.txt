package com.datastudioasteroids.alma_paid_admin.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "courses")
data class Course(
    @PrimaryKey val id: Long,
    val title: String,
    val baseFee: Double,
    val dueDay: Int,
    val latePctPerDay: Double
)
