package com.datastudioasteroids.alma_paid_admin.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.datastudioasteroids.alma_paid_admin.data.dao.*
import com.datastudioasteroids.alma_paid_admin.data.model.*

@Database(
    entities = [Student::class, Course::class, Enrollment::class, Invoice::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun studentDao(): StudentDao
    abstract fun courseDao(): CourseDao
    abstract fun enrollmentDao(): EnrollmentDao
    abstract fun invoiceDao(): InvoiceDao

    companion object {
        @Volatile private var INST: AppDatabase? = null
        fun getDatabase(ctx: Context): AppDatabase =
            INST ?: synchronized(this) {
                Room.databaseBuilder(
                    ctx.applicationContext,
                    AppDatabase::class.java,
                    "alma_paid_db"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                    .also { INST = it }
            }
    }
}
