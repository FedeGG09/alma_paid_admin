package com.datastudioasteroids.alma_paid_admin.ui

import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.datastudioasteroids.alma_paid_admin.databinding.ActivityMainBinding
import com.datastudioasteroids.alma_paid_admin.ui.adapters.InvoiceAdapter

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private val vm: MainViewModel by viewModels {
        MainViewModelFactory((application as AlmaPaidApp).repository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val adapter = InvoiceAdapter { id -> vm.markPaid(id) }
        binding.rvPending.layoutManager = LinearLayoutManager(this)
        binding.rvPending.adapter = adapter

        vm.pendingInvoices.observe(this) { adapter.submitList(it) }

        binding.syncButton.setOnClickListener { vm.sync() }
        vm.sync()
    }
}
