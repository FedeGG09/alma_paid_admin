package com.datastudioasteroids.alma_paid_admin.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "students")
data class Student(
    @PrimaryKey val dni: String,
    val name: String
)
