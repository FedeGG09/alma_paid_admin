package com.datastudioasteroids.alma_paid_admin.ui

import androidx.lifecycle.*
import com.datastudioasteroids.alma_paid_admin.data.model.Invoice
import com.datastudioasteroids.alma_paid_admin.repository.DataRepository
import kotlinx.coroutines.launch

class MainViewModel(private val repo: DataRepository) : ViewModel() {

    val pendingInvoices: LiveData<List<Invoice>> =
        repo.getPendingInvoices().asLiveData()

    val paidInvoices: LiveData<List<Invoice>> =
        repo.getPaidInvoices().asLiveData()

    fun sync() = viewModelScope.launch { repo.fetchAndSyncAll() }

    fun markPaid(id: Long) = viewModelScope.launch { repo.markAsPaid(id) }
}
