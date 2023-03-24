odoo.define('crm_dashboard.', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var session = require('web.session')
    var year_win_loss=[]
    var month_win_loss=[]
    var week_win_loss=[]
    var quarter_win_loss=[]
    var CrmDashboard = AbstractAction.extend({
        template: 'DashboardCrm',
        events: {
            'click .my_lead': 'my_lead',
            'click .opportunity': 'opportunity',
            'change #income_expense_values': function (e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value == "this_year") {
                    this.onclick_this_year($target.val());

                }
                else if (value == "this_quarter") {
                    this.onclick_this_quarter($target.val());
                }
                else if (value == "this_month") {
                    this.onclick_this_month($target.val());
                }
                else if (value == "this_week") {
                    this.onclick_this_week($target.val());
                }
            },
        },
        init: function (parent, action) {
            this._super(parent, action);
        },
        start: function () {

            var self = this;
            this._super().then(function () {

            }),


                rpc.query({
                    model: 'crm.lead',
                    method: 'crm_lead',
                    args: [],
                }).then(function (result) {
                    $('#my_leads').append('<span>' + result.lead + '</span>');
                    $('#my_opportunities').append('<span>' + result.opportunity + '</span>');
                    $('#expected_revenue').append('<span>' + result.expected_revenue + '</span>');
                    $('#revenue').append('<span>' + result.revenue + '</span>');
                    $('#win_ratio').append('<span>' + result.win_ratio + '</span>');

                })

        },


        onclick_this_year: function (ev) {
            var self = this;


            rpc.query({
                model: 'crm.lead',
                method: 'crm_year',
                args: [],
            })
                .then(function (result) {
                    $('#my_leads').empty()
                    $('#my_opportunities').empty()
                    $('#expected_revenue').empty()
                    $('#revenue').empty()
                    $('#win_ratio').empty()

                    $('#my_leads').append('<span>' + result.lead_year + '</span>');
                    $('#my_opportunities').append('<span>' + result.opportunity_year + '</span>');
                    $('#expected_revenue').append('<span>' + result.expected_rev_year + '</span>');
                    $('#revenue').append('<span>' + result.year_revenue + '</span>');
                    $('#win_ratio').append('<span>' + result.year_win_ratio + '</span>');

                    $("#weekChart").hide()
                    $('#monthChart').hide()
                    $('#quarterChart').hide()
                    $('#yearChart').show();

                    $('#year_crm_activity').show()
                    $('#month_crm_activity').hide()
                    $('#quarter_crm_activity').hide()
                    $('#week_crm_activity').hide()

                    year_win_loss.push(result.year_win_manager_count,result.year_loss_manager_count)
                    self.render_year_won_loss();
                    self.render_year_crm_activity();





                })
        },

        onclick_this_month: function (ev) {

            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_month',
                args: [],
            })
                .then(function (result) {
                    $('#my_leads').empty()
                    $('#my_opportunities').empty()
                    $('#expected_revenue').empty()
                    $('#revenue').empty()
                    $('#win_ratio').empty()

                    $('#my_leads').append('<span>' + result.month_lead_count + '</span>');
                    $('#my_opportunities').append('<span>' + result.month_opp_count + '</span>');
                    $('#expected_revenue').append('<span>' + result.month_expected_revenue + '</span>');
                    $('#revenue').append('<span>' + result.month_revenue + '</span>');
                    $('#win_ratio').append('<span>' + result.month_win_ratio + '</span>');

                    $("#weekChart").hide()
                    $('#quarterChart').hide()
                    $('#yearChart').hide()
                    $('#monthChart').show()

                    $('#year_crm_activity').hide()
                    $('#week_crm_activity').hide()
                    $('#quarter_crm_activity').hide()
                    $('#month_crm_activity').show()

                    month_win_loss.push(result.month_win_manager_count,result.month_loss_manager_count)
                    self.render_month_won_loss()
                    self.render_month_crm_activity();






                })
        },

        onclick_this_week: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_week',
                args: [],
            })
                .then(function (result) {
                    $('#my_leads').empty()
                    $('#my_opportunities').empty()
                    $('#expected_revenue').empty()
                    $('#revenue').empty()
                    $('#win_ratio').empty()

                    $('#my_leads').append('<span>' + result.week_lead_count + '</span>');
                    $('#my_opportunities').append('<span>' + result.week_opp_count + '</span>');
                    $('#expected_revenue').append('<span>' + result.week_expected_revenue + '</span>');
                    $('#revenue').append('<span>' + result.week_revenue + '</span>');
                    $('#win_ratio').append('<span>' + result.week_win_ratio + '</span>');


                    $('#yearChart').hide()
                    $('#monthChart').hide()
                    $('#quarterChart').hide()
                    $("#weekChart").show()

                    $('#year_crm_activity').hide()
                    $('#month_crm_activity').hide()
                    $('#quarter_crm_activity').hide()
                    $('#week_crm_activity').show()
                    week_win_loss.push(result.week_win_manager_count,result.week_loss_manager_count)
                    self.render_week_won_loss()
                    self.render_week_crm_activity()


                })
        },

        onclick_this_quarter: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_quarter',
                args: [],
            })
                .then(function (result) {
                    $('#my_leads').empty()
                    $('#my_opportunities').empty()
                    $('#expected_revenue').empty()
                    $('#revenue').empty()
                    $('#win_ratio').empty()

                    $('#my_leads').append('<span>' + result.quarter_lead_count + '</span>');
                    $('#my_opportunities').append('<span>' + result.quarter_opp_count + '</span>');
                    $('#expected_revenue').append('<span>' + result.quarter_expected_revenue + '</span>');
                    $('#revenue').append('<span>' + result.quarter_revenue + '</span>');
                    $('#win_ratio').append('<span>' + result.quarter_win_ratio + '</span>');

                    $('#yearChart').hide()
                    $('#monthChart').hide()
                    $("#weekChart").hide()
                    $('#quarterChart').show()

                    $('#year_crm_activity').hide()
                    $('#month_crm_activity').hide()
                    $('#quarter_crm_activity').show()
                    $('#week_crm_activity').hide()


                    quarter_win_loss.push(result.quarter_win_manager_count,result.quarter_loss_manager_count)
                    self.render_quarter_won_loss()
                    self.render_quarter_crm_activity()
                })
        },






        render_year_won_loss: function () {

            const ctx = $('#yearChart')
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Won', 'Loss'],
                    datasets: [{
                        label: '',
                        data: year_win_loss,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },

        render_month_won_loss: function () {

            const ctx = $('#monthChart')
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Won', 'Loss'],
                    datasets: [{
                        label: '',
                        data: month_win_loss,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },

    render_week_won_loss: function () {
            const ctx = $('#weekChart')
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Won', 'Loss'],
                    datasets: [{
                        label: '',
                        data: week_win_loss,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },

        render_quarter_won_loss: function () {
            const ctx = $('#quarterChart')
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Won', 'Loss'],
                    datasets: [{
                        label: '',
                        data: quarter_win_loss,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },


        render_year_crm_activity: function () {
            rpc.query({
                model: "crm.lead",
                method: "get_year_crm_activity",
            }).then(function (result) {
                var label = []
                var data1 = []
                $.each(result, function (index, name) {
                    label.push(index)
                    data1.push(name)
                })
                const ctx = $('#year_crm_activity')
                new Chart(ctx, {

                    type: 'bar',

                    data: {
                        labels: label,
                        datasets: [{
                            label: '',
                            data: data1,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
        },

        render_month_crm_activity: function () {
            rpc.query({
                model: "crm.lead",
                method: "get_month_crm_activity",
            }).then(function (result) {
                var label = []
                var data1 = []
                $.each(result, function (index, name) {
                    label.push(index)
                    data1.push(name)
                })
                const ctx = $('#month_crm_activity')
                new Chart(ctx, {

                    type: 'bar',

                    data: {
                        labels: label,
                        datasets: [{
                            label: '',
                            data: data1,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
        },

        render_week_crm_activity: function () {
            rpc.query({
                model: "crm.lead",
                method: "get_week_crm_activity",
            }).then(function (result) {
                var label = []
                var data1 = []
                $.each(result, function (index, name) {
                    label.push(index)
                    data1.push(name)
                })
                const ctx = $('#week_crm_activity')
                new Chart(ctx, {

                    type: 'bar',

                    data: {
                        labels: label,
                        datasets: [{
                            label: '',
                            data: data1,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
        },

        render_quarter_crm_activity: function () {
            rpc.query({
                model: "crm.lead",
                method: "get_quarter_crm_activity",
            }).then(function (result) {
                var label = []
                var data1 = []
                $.each(result, function (index, name) {
                    label.push(index)
                    data1.push(name)
                })
                const ctx = $('#quarter_crm_activity')
                new Chart(ctx, {

                    type: 'bar',

                    data: {
                        labels: label,
                        datasets: [{
                            label: '',
                            data: data1,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
        },







        my_lead: function (e) {
            this.do_action({
                name: "My Leads",
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'], [false, 'form']],
                domain: [['user_id', '=', session.uid], ['type', '=', 'lead']],
                target: 'current',
            })
        },

        opportunity: function (e) {
            this.do_action({
                name: 'Opportunity',
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: [['user_id', '=', session.uid], ['type', '=', 'opportunity']],
                target: 'current',
            })
        },








    });
    core.action_registry.add("crm_dashboard", CrmDashboard);
    return CrmDashboard;
});