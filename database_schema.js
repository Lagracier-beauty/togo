// ===== SCHÉMA DE BASE DE DONNÉES TOG-SERVICES =====
// Modèles convertis de Django vers JavaScript pour db.docs

const databaseSchema = {
  // ===== MODÈLE UTILISATEUR DJANGO (User) =====
  User: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      username: { type: "CharField", max_length: 150, unique: true },
      email: { type: "EmailField", max_length: 254, unique: true },
      first_name: { type: "CharField", max_length: 150 },
      last_name: { type: "CharField", max_length: 150 },
      password: { type: "CharField", max_length: 128 },
      is_staff: { type: "BooleanField", default: false },
      is_superuser: { type: "BooleanField", default: false },
      is_active: { type: "BooleanField", default: true },
      date_joined: { type: "DateTimeField", auto_now_add: true },
      last_login: { type: "DateTimeField", null: true }
    },
    relations: {
      profile: { type: "OneToOne", model: "UserProfile", related_name: "user" },
      addresses: { type: "OneToMany", model: "UserAddress", related_name: "user" },
      notifications: { type: "OneToMany", model: "Notification", related_name: "user" },
      sessions: { type: "OneToMany", model: "UserSession", related_name: "user" },
      customer_chats: { type: "OneToMany", model: "Chat", related_name: "customer" },
      orders: { type: "OneToMany", model: "Order", related_name: "customer" },
      support_tickets: { type: "OneToMany", model: "SupportTicket", related_name: "user" },
      assigned_tickets: { type: "OneToMany", model: "SupportTicket", related_name: "assigned_to" },
      transactions: { type: "OneToMany", model: "Transaction", related_name: "user" },
      payment_methods: { type: "OneToMany", model: "UserPaymentMethod", related_name: "user" },
      customer_disputes: { type: "OneToMany", model: "Dispute", related_name: "customer" },
      mediated_disputes: { type: "OneToMany", model: "Dispute", related_name: "mediator" }
    }
  },

  // ===== MODÈLES UTILISATEURS (users app) =====
  UserProfile: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      phone: { type: "CharField", max_length: 20, null: true },
      phone_verified: { type: "BooleanField", default: false },
      phone_verification_code: { type: "CharField", max_length: 6, null: true },
      phone_verification_expires: { type: "DateTimeField", null: true },
      profile_picture: { type: "ImageField", upload_to: "profile_pictures/", null: true },
      date_of_birth: { type: "DateField", null: true },
      gender: { type: "CharField", max_length: 10, choices: ["male", "female", "other"], null: true },
      address: { type: "TextField", null: true },
      city: { type: "CharField", max_length: 100, null: true },
      postal_code: { type: "CharField", max_length: 10, null: true },
      country: { type: "CharField", max_length: 50, default: "Togo" },
      current_latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      current_longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      location_updated_at: { type: "DateTimeField", null: true },
      preferred_language: { type: "CharField", max_length: 10, choices: ["fr", "en", "ee"], default: "fr" },
      preferred_currency: { type: "CharField", max_length: 5, default: "XOF" },
      email_notifications: { type: "BooleanField", default: true },
      sms_notifications: { type: "BooleanField", default: true },
      push_notifications: { type: "BooleanField", default: true },
      is_verified: { type: "BooleanField", default: false },
      is_premium: { type: "BooleanField", default: false },
      premium_expires: { type: "DateTimeField", null: true },
      google_id: { type: "CharField", max_length: 100, null: true },
      facebook_id: { type: "CharField", max_length: 100, null: true },
      total_orders: { type: "PositiveIntegerField", default: 0 },
      total_spent: { type: "DecimalField", max_digits: 12, decimal_places: 2, default: 0 },
      average_rating_given: { type: "DecimalField", max_digits: 3, decimal_places: 2, default: 0 },
      created_at: { type: "DateTimeField", auto_now_add: true },
      updated_at: { type: "DateTimeField", auto_now: true }
    },
    relations: {
      user: { type: "OneToOne", model: "User", related_name: "profile" }
    }
  },

  UserAddress: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      type: { type: "CharField", max_length: 10, choices: ["home", "work", "other"], default: "other" },
      name: { type: "CharField", max_length: 100 },
      address: { type: "TextField" },
      city: { type: "CharField", max_length: 100 },
      postal_code: { type: "CharField", max_length: 10, null: true },
      latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      is_default: { type: "BooleanField", default: false },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      user: { type: "ManyToOne", model: "User", related_name: "addresses" }
    }
  },

  Notification: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      title: { type: "CharField", max_length: 200 },
      message: { type: "TextField" },
      notification_type: { type: "CharField", max_length: 20, choices: ["order_status", "payment", "message", "promotion", "system", "reminder"] },
      is_read: { type: "BooleanField", default: false },
      is_sent_email: { type: "BooleanField", default: false },
      is_sent_sms: { type: "BooleanField", default: false },
      is_sent_push: { type: "BooleanField", default: false },
      send_at: { type: "DateTimeField", null: true },
      data: { type: "JSONField", default: {} },
      created_at: { type: "DateTimeField", auto_now_add: true },
      read_at: { type: "DateTimeField", null: true }
    },
    relations: {
      user: { type: "ManyToOne", model: "User", related_name: "notifications" },
      order: { type: "ManyToOne", model: "Order", related_name: "notifications", null: true }
    }
  },

  UserSession: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      session_key: { type: "CharField", max_length: 40, unique: true },
      device_type: { type: "CharField", max_length: 20, choices: ["web", "mobile", "tablet", "desktop"], default: "web" },
      device_info: { type: "TextField", null: true },
      ip_address: { type: "GenericIPAddressField" },
      location_city: { type: "CharField", max_length: 100, null: true },
      location_country: { type: "CharField", max_length: 100, null: true },
      is_active: { type: "BooleanField", default: true },
      last_activity: { type: "DateTimeField", auto_now: true },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      user: { type: "ManyToOne", model: "User", related_name: "sessions" }
    }
  },

  Chat: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      chat_type: { type: "CharField", max_length: 10, choices: ["order", "support", "general"], default: "order" },
      is_active: { type: "BooleanField", default: true },
      created_at: { type: "DateTimeField", auto_now_add: true },
      last_message_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      customer: { type: "ManyToOne", model: "User", related_name: "customer_chats" },
      provider: { type: "ManyToOne", model: "Provider", related_name: "provider_chats" },
      order: { type: "ManyToOne", model: "Order", related_name: "chats", null: true },
      messages: { type: "OneToMany", model: "ChatMessage", related_name: "chat" }
    }
  },

  ChatMessage: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      message_type: { type: "CharField", max_length: 10, choices: ["text", "image", "location", "system"], default: "text" },
      content: { type: "TextField", null: true },
      attachment: { type: "FileField", upload_to: "chat_attachments/", null: true },
      latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      is_read: { type: "BooleanField", default: false },
      is_system: { type: "BooleanField", default: false },
      created_at: { type: "DateTimeField", auto_now_add: true },
      read_at: { type: "DateTimeField", null: true }
    },
    relations: {
      chat: { type: "ManyToOne", model: "Chat", related_name: "messages" },
      sender: { type: "ManyToOne", model: "User", related_name: "sent_messages" }
    }
  },

  // ===== MODÈLES PRESTATAIRES (providers app) =====
  Provider: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      service_type: { type: "CharField", max_length: 20, choices: ["livraison", "transport", "menage", "bricolage", "autre"] },
      description: { type: "TextField", null: true },
      experience_years: { type: "PositiveIntegerField", default: 0 },
      hourly_rate: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      is_available: { type: "BooleanField", default: true },
      status: { type: "CharField", max_length: 20, choices: ["pending", "approved", "rejected", "suspended"], default: "pending" },
      rating: { type: "DecimalField", max_digits: 3, decimal_places: 2, default: 0 },
      total_services: { type: "PositiveIntegerField", default: 0 },
      created_at: { type: "DateTimeField", auto_now_add: true },
      updated_at: { type: "DateTimeField", auto_now: true }
    },
    relations: {
      user: { type: "OneToOne", model: "User", related_name: "provider_profile" },
      documents: { type: "OneToMany", model: "ProviderDocument", related_name: "provider" },
      zones: { type: "OneToMany", model: "ProviderZone", related_name: "provider" },
      services: { type: "OneToMany", model: "Service", related_name: "provider" },
      received_orders: { type: "OneToMany", model: "Order", related_name: "provider" },
      provider_chats: { type: "OneToMany", model: "Chat", related_name: "provider" },
      earnings: { type: "OneToMany", model: "ProviderEarnings", related_name: "provider" },
      withdrawal_requests: { type: "OneToMany", model: "WithdrawalRequest", related_name: "provider" },
      provider_disputes: { type: "OneToMany", model: "Dispute", related_name: "provider" }
    }
  },

  ProviderDocument: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      document_type: { type: "CharField", max_length: 20, choices: ["cni", "passport", "license", "certificate", "other"] },
      file: { type: "FileField", upload_to: "provider_documents/" },
      is_verified: { type: "BooleanField", default: false },
      uploaded_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      provider: { type: "ManyToOne", model: "Provider", related_name: "documents" }
    }
  },

  ProviderZone: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      city: { type: "CharField", max_length: 100 },
      neighborhood: { type: "CharField", max_length: 100, null: true },
      is_active: { type: "BooleanField", default: true }
    },
    relations: {
      provider: { type: "ManyToOne", model: "Provider", related_name: "zones" }
    }
  },

  // ===== MODÈLES SERVICES (services app) =====
  ServiceCategory: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      name: { type: "CharField", max_length: 100, unique: true },
      description: { type: "TextField", null: true },
      icon: { type: "CharField", max_length: 50 },
      color: { type: "CharField", max_length: 7, default: "#007bff" },
      is_active: { type: "BooleanField", default: true },
      order: { type: "PositiveIntegerField", default: 0 },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      services: { type: "OneToMany", model: "Service", related_name: "category" }
    }
  },

  Service: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      title: { type: "CharField", max_length: 200 },
      description: { type: "TextField" },
      pricing_type: { type: "CharField", max_length: 20, choices: ["fixed", "hourly", "distance", "custom"] },
      base_price: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      min_price: { type: "DecimalField", max_digits: 10, decimal_places: 2, null: true },
      max_price: { type: "DecimalField", max_digits: 10, decimal_places: 2, null: true },
      duration_minutes: { type: "PositiveIntegerField", null: true },
      is_instant: { type: "BooleanField", default: false },
      is_bookable: { type: "BooleanField", default: true },
      max_advance_days: { type: "PositiveIntegerField", default: 30 },
      is_active: { type: "BooleanField", default: true },
      featured: { type: "BooleanField", default: false },
      created_at: { type: "DateTimeField", auto_now_add: true },
      updated_at: { type: "DateTimeField", auto_now: true }
    },
    relations: {
      category: { type: "ManyToOne", model: "ServiceCategory", related_name: "services" },
      provider: { type: "ManyToOne", model: "Provider", related_name: "services" },
      images: { type: "OneToMany", model: "ServiceImage", related_name: "service" },
      availability: { type: "OneToMany", model: "ServiceAvailability", related_name: "service" },
      orders: { type: "OneToMany", model: "Order", related_name: "service" }
    }
  },

  ServiceImage: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      image: { type: "ImageField", upload_to: "service_images/" },
      caption: { type: "CharField", max_length: 200, null: true },
      is_primary: { type: "BooleanField", default: false },
      uploaded_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      service: { type: "ManyToOne", model: "Service", related_name: "images" }
    }
  },

  ServiceAvailability: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      weekday: { type: "IntegerField", choices: [0, 1, 2, 3, 4, 5, 6] },
      start_time: { type: "TimeField" },
      end_time: { type: "TimeField" },
      is_available: { type: "BooleanField", default: true }
    },
    relations: {
      service: { type: "ManyToOne", model: "Service", related_name: "availability" }
    }
  },

  // ===== MODÈLES COMMANDES (orders app) =====
  Order: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      order_number: { type: "CharField", max_length: 20, unique: true },
      status: { type: "CharField", max_length: 20, choices: ["pending", "accepted", "rejected", "in_progress", "on_route", "arrived", "completed", "cancelled", "disputed"], default: "pending" },
      priority: { type: "CharField", max_length: 10, choices: ["low", "medium", "high"], default: "low" },
      description: { type: "TextField" },
      special_instructions: { type: "TextField", null: true },
      pickup_address: { type: "TextField", null: true },
      pickup_latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      pickup_longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      delivery_address: { type: "TextField", null: true },
      delivery_latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      delivery_longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      scheduled_datetime: { type: "DateTimeField", null: true },
      estimated_duration: { type: "PositiveIntegerField", null: true },
      estimated_price: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      final_price: { type: "DecimalField", max_digits: 10, decimal_places: 2, null: true },
      additional_fees: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      total_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2, null: true },
      created_at: { type: "DateTimeField", auto_now_add: true },
      accepted_at: { type: "DateTimeField", null: true },
      started_at: { type: "DateTimeField", null: true },
      completed_at: { type: "DateTimeField", null: true },
      customer_notes: { type: "TextField", null: true },
      provider_notes: { type: "TextField", null: true },
      admin_notes: { type: "TextField", null: true }
    },
    relations: {
      customer: { type: "ManyToOne", model: "User", related_name: "orders" },
      service: { type: "ManyToOne", model: "Service", related_name: "orders" },
      provider: { type: "ManyToOne", model: "Provider", related_name: "received_orders" },
      tracking: { type: "OneToMany", model: "OrderTracking", related_name: "order" },
      images: { type: "OneToMany", model: "OrderImage", related_name: "order" },
      rating: { type: "OneToOne", model: "OrderRating", related_name: "order" },
      chats: { type: "OneToMany", model: "Chat", related_name: "order" },
      transactions: { type: "OneToMany", model: "Transaction", related_name: "order" },
      provider_earnings: { type: "OneToMany", model: "ProviderEarnings", related_name: "order" },
      support_tickets: { type: "OneToMany", model: "SupportTicket", related_name: "order" },
      dispute: { type: "OneToOne", model: "Dispute", related_name: "order" },
      notifications: { type: "OneToMany", model: "Notification", related_name: "order" }
    }
  },

  OrderTracking: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      status: { type: "CharField", max_length: 20, choices: ["pending", "accepted", "rejected", "in_progress", "on_route", "arrived", "completed", "cancelled", "disputed"] },
      message: { type: "TextField", null: true },
      latitude: { type: "DecimalField", max_digits: 10, decimal_places: 8, null: true },
      longitude: { type: "DecimalField", max_digits: 11, decimal_places: 8, null: true },
      timestamp: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      order: { type: "ManyToOne", model: "Order", related_name: "tracking" }
    }
  },

  OrderImage: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      image: { type: "ImageField", upload_to: "order_images/" },
      caption: { type: "CharField", max_length: 200, null: true },
      is_before: { type: "BooleanField", default: true },
      uploaded_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      order: { type: "ManyToOne", model: "Order", related_name: "images" },
      uploaded_by: { type: "ManyToOne", model: "User", related_name: "uploaded_order_images" }
    }
  },

  OrderRating: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      customer_rating: { type: "PositiveIntegerField", choices: [1, 2, 3, 4, 5], null: true },
      customer_comment: { type: "TextField", null: true },
      provider_rating: { type: "PositiveIntegerField", choices: [1, 2, 3, 4, 5], null: true },
      provider_comment: { type: "TextField", null: true },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      order: { type: "OneToOne", model: "Order", related_name: "rating" }
    }
  },

  // ===== MODÈLES PAIEMENTS (payments app) =====
  PaymentMethod: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      name: { type: "CharField", max_length: 100 },
      payment_type: { type: "CharField", max_length: 20, choices: ["mobile_money", "credit_card", "debit_card", "bank_transfer", "cash"] },
      provider: { type: "CharField", max_length: 20, choices: ["tmoney", "flooz", "visa", "mastercard", "stripe", "paypal"] },
      is_active: { type: "BooleanField", default: true },
      processing_fee_percent: { type: "DecimalField", max_digits: 5, decimal_places: 2, default: 0 },
      processing_fee_fixed: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      icon: { type: "CharField", max_length: 50 },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      user_payment_methods: { type: "OneToMany", model: "UserPaymentMethod", related_name: "payment_method" },
      transactions: { type: "OneToMany", model: "Transaction", related_name: "payment_method" },
      withdrawal_requests: { type: "OneToMany", model: "WithdrawalRequest", related_name: "payment_method" }
    }
  },

  UserPaymentMethod: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      account_number: { type: "CharField", max_length: 100 },
      account_name: { type: "CharField", max_length: 100, null: true },
      is_default: { type: "BooleanField", default: false },
      is_verified: { type: "BooleanField", default: false },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      user: { type: "ManyToOne", model: "User", related_name: "payment_methods" },
      payment_method: { type: "ManyToOne", model: "PaymentMethod", related_name: "user_payment_methods" }
    }
  },

  Transaction: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      transaction_id: { type: "CharField", max_length: 100, unique: true },
      external_transaction_id: { type: "CharField", max_length: 100, null: true },
      transaction_type: { type: "CharField", max_length: 20, choices: ["payment", "commission", "payout", "refund", "withdrawal"] },
      status: { type: "CharField", max_length: 20, choices: ["pending", "processing", "completed", "failed", "cancelled", "refunded"], default: "pending" },
      amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      processing_fee: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      platform_commission: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      net_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      description: { type: "TextField", null: true },
      metadata: { type: "JSONField", default: {} },
      failure_reason: { type: "TextField", null: true },
      created_at: { type: "DateTimeField", auto_now_add: true },
      processed_at: { type: "DateTimeField", null: true },
      completed_at: { type: "DateTimeField", null: true }
    },
    relations: {
      order: { type: "ManyToOne", model: "Order", related_name: "transactions", null: true },
      user: { type: "ManyToOne", model: "User", related_name: "transactions" },
      payment_method: { type: "ManyToOne", model: "PaymentMethod", related_name: "transactions" },
      provider_earnings: { type: "OneToMany", model: "ProviderEarnings", related_name: "transaction" }
    }
  },

  ProviderEarnings: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      gross_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      platform_commission: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      net_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      is_paid: { type: "BooleanField", default: false },
      paid_at: { type: "DateTimeField", null: true },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      provider: { type: "ManyToOne", model: "Provider", related_name: "earnings" },
      order: { type: "ManyToOne", model: "Order", related_name: "provider_earnings" },
      transaction: { type: "ManyToOne", model: "Transaction", related_name: "provider_earnings" }
    }
  },

  WithdrawalRequest: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      account_number: { type: "CharField", max_length: 100 },
      amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      processing_fee: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      net_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2 },
      status: { type: "CharField", max_length: 20, choices: ["pending", "approved", "rejected", "completed"], default: "pending" },
      notes: { type: "TextField", null: true },
      admin_notes: { type: "TextField", null: true },
      requested_at: { type: "DateTimeField", auto_now_add: true },
      processed_at: { type: "DateTimeField", null: true },
      completed_at: { type: "DateTimeField", null: true }
    },
    relations: {
      provider: { type: "ManyToOne", model: "Provider", related_name: "withdrawal_requests" },
      payment_method: { type: "ManyToOne", model: "PaymentMethod", related_name: "withdrawal_requests" }
    }
  },

  // ===== MODÈLES SUPPORT (support app) =====
  FAQ: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      category: { type: "CharField", max_length: 20, choices: ["general", "account", "orders", "payments", "providers", "technical"] },
      question: { type: "TextField" },
      answer: { type: "TextField" },
      is_featured: { type: "BooleanField", default: false },
      order: { type: "PositiveIntegerField", default: 0 },
      views_count: { type: "PositiveIntegerField", default: 0 },
      is_active: { type: "BooleanField", default: true },
      created_at: { type: "DateTimeField", auto_now_add: true },
      updated_at: { type: "DateTimeField", auto_now: true }
    }
  },

  SupportTicket: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      ticket_number: { type: "CharField", max_length: 20, unique: true },
      subject: { type: "CharField", max_length: 200 },
      description: { type: "TextField" },
      category: { type: "CharField", max_length: 20, choices: ["general", "account", "order", "payment", "provider", "technical", "dispute", "other"] },
      priority: { type: "CharField", max_length: 10, choices: ["low", "medium", "high", "urgent"], default: "medium" },
      status: { type: "CharField", max_length: 20, choices: ["open", "in_progress", "waiting_user", "waiting_provider", "resolved", "closed"], default: "open" },
      created_at: { type: "DateTimeField", auto_now_add: true },
      updated_at: { type: "DateTimeField", auto_now: true },
      resolved_at: { type: "DateTimeField", null: true },
      closed_at: { type: "DateTimeField", null: true },
      satisfaction_rating: { type: "PositiveIntegerField", choices: [1, 2, 3, 4, 5], null: true },
      satisfaction_comment: { type: "TextField", null: true }
    },
    relations: {
      user: { type: "ManyToOne", model: "User", related_name: "support_tickets" },
      order: { type: "ManyToOne", model: "Order", related_name: "support_tickets", null: true },
      assigned_to: { type: "ManyToOne", model: "User", related_name: "assigned_tickets", null: true },
      messages: { type: "OneToMany", model: "SupportMessage", related_name: "ticket" },
      attachments: { type: "OneToMany", model: "SupportAttachment", related_name: "ticket" }
    }
  },

  SupportMessage: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      message: { type: "TextField" },
      is_internal: { type: "BooleanField", default: false },
      is_system: { type: "BooleanField", default: false },
      created_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      ticket: { type: "ManyToOne", model: "SupportTicket", related_name: "messages" },
      sender: { type: "ManyToOne", model: "User", related_name: "support_messages" },
      attachments: { type: "OneToMany", model: "SupportAttachment", related_name: "message" }
    }
  },

  SupportAttachment: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      file: { type: "FileField", upload_to: "support_attachments/" },
      filename: { type: "CharField", max_length: 255 },
      file_size: { type: "PositiveIntegerField" },
      uploaded_at: { type: "DateTimeField", auto_now_add: true }
    },
    relations: {
      ticket: { type: "ManyToOne", model: "SupportTicket", related_name: "attachments" },
      message: { type: "ManyToOne", model: "SupportMessage", related_name: "attachments", null: true },
      uploaded_by: { type: "ManyToOne", model: "User", related_name: "support_attachments" }
    }
  },

  Dispute: {
    fields: {
      id: { type: "AutoField", primary_key: true },
      dispute_type: { type: "CharField", max_length: 20, choices: ["service_quality", "no_show", "payment", "pricing", "damage", "behavior", "other"] },
      customer_description: { type: "TextField" },
      provider_response: { type: "TextField", null: true },
      admin_notes: { type: "TextField", null: true },
      status: { type: "CharField", max_length: 20, choices: ["open", "investigating", "mediation", "resolved", "closed"], default: "open" },
      resolution: { type: "CharField", max_length: 20, choices: ["refund_full", "refund_partial", "service_redo", "provider_warning", "provider_suspension", "no_action", "other"], null: true },
      resolution_notes: { type: "TextField", null: true },
      refund_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      compensation_amount: { type: "DecimalField", max_digits: 10, decimal_places: 2, default: 0 },
      created_at: { type: "DateTimeField", auto_now_add: true },
      resolved_at: { type: "DateTimeField", null: true },
      closed_at: { type: "DateTimeField", null: true }
    },
    relations: {
      order: { type: "OneToOne", model: "Order", related_name: "dispute" },
      customer: { type: "ManyToOne", model: "User", related_name: "customer_disputes" },
      provider: { type: "ManyToOne", model: "Provider", related_name: "provider_disputes" },
      mediator: { type: "ManyToOne", model: "User", related_name: "mediated_disputes", null: true }
    }
  }
};

// Export pour db.docs
module.exports = databaseSchema; 