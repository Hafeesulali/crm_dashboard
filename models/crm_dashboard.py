from odoo import fields, models, api
from odoo.tools import date_utils


class SalesTeamInherit(models.Model):
    _inherit = "crm.team"

    crm_state_id = fields.Many2one("crm.stage")


class SaleInherit(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        super(SaleInherit, self).action_confirm()
        self.team_id.crm_state_id = self.opportunity_id.stage_id


class CrmLead(models.Model):
    _inherit = "crm.lead"

    crm_manager_id = fields.Many2one("res.users", string="Crm Manager")

    @api.model
    def crm_lead(self):
        """lead,opportunity,expected revenue,revenue,win ratio card values"""
        record = {}
        lead_count = self.env["crm.lead"].search_count([('type', '=', 'lead'), ('user_id', '=', self.env.user.id)])
        opportunity_count = self.env["crm.lead"].search_count(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id)])
        expected_revenue = sum(
            self.env["crm.lead"].search([('user_id', '=', self.env.user.id)]).mapped('expected_revenue'))
        revenue = round(sum(self.env["sale.order"].search([('user_id', '=', self.env.user.id)]).mapped("amount_total")),
                        2)
        win_count = (self.env["crm.lead"]).search_count(
            [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id)])
        win_ratio = round((win_count / (lead_count + opportunity_count)) * 100, 2)

        record.update({
            "lead": lead_count,
            "opportunity": opportunity_count,
            "expected_revenue": expected_revenue,
            "revenue": revenue,
            "win_ratio": win_ratio
        })

        return record

    @api.model
    def crm_year(self):
        rec = {}
        lead_count = self.search([('type', '=', 'lead'), ('user_id', '=', self.env.user.id)])
        year_lead_count = len(
            [record.create_date.year for record in lead_count if fields.Date.today().year == record.create_date.year])

        opportunity_count = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id)])
        year_opp_count = len(
            [record.create_date.year for record in opportunity_count if
             fields.Date.today().year == record.create_date.year])

        year_expected_revenue = sum(self.env["crm.lead"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year).mapped("expected_revenue"))
        year_revenue = round(sum(self.env["sale.order"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year).mapped("amount_total")),
                             2)
        year_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year)
        year_win_list = len([i.id for i in year_win_count])
        year_win_ratio = round((year_win_list / (year_lead_count + year_opp_count)) * 100, 2)
        year_win_manager = (self.env["crm.lead"]).search([('stage_id.is_won', '=', True)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year)
        year_win_manager_count = len([i.id for i in year_win_manager])
        year_loss_manager = (self.env["crm.lead"]).search(
            [('active', '=', False)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year)
        year_loss_manager_count = len([i.id for i in year_loss_manager])

        rec.update({
            'lead_year': year_lead_count,
            'opportunity_year': year_opp_count,
            'expected_rev_year': year_expected_revenue,
            'year_revenue': year_revenue,
            'year_win_ratio': year_win_ratio,
            "year_win_manager_count": year_win_manager_count,
            "year_loss_manager_count": year_loss_manager_count

        })

        return rec

    @api.model
    def crm_month(self):
        rec = {}
        month_lead = self.env["crm.lead"].search(
            [('type', '=', 'lead'), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_lead_count = len([i.id for i in month_lead])

        month_opportunity = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_opp_count = len([i.id for i in month_opportunity])

        month_expected_revenue = sum(self.env["crm.lead"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month).mapped("expected_revenue"))
        month_revenue = round(sum(self.env["sale.order"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month).mapped("amount_total")),
                              2)
        month_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_win_list = len([i.id for i in month_win_count])
        month_win_ratio = round((month_win_list / (month_lead_count + month_opp_count)) * 100, 2)
        month_win_manager = (self.env["crm.lead"]).search([('stage_id.is_won', '=', True)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_win_manager_count = len([i.id for i in month_win_manager])
        month_loss_manager = (self.env["crm.lead"]).search(
            [('active', '=', False)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_loss_manager_count = len([i.id for i in month_loss_manager])

        rec.update({
            "month_lead_count": month_lead_count,
            "month_opp_count": month_opp_count,
            "month_expected_revenue": month_expected_revenue,
            "month_revenue": month_revenue,
            "month_win_ratio": month_win_ratio,
            "month_win_manager_count": month_win_manager_count,
            "month_loss_manager_count": month_loss_manager_count,

        })

        return rec

    @api.model
    def crm_week(self):
        rec = {}
        week_lead = self.env["crm.lead"].search(
            [('type', '=', 'lead'), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_lead_count = len([i.id for i in week_lead])

        week_opportunity = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_opp_count = len([i.id for i in week_opportunity])

        week_expected_revenue = sum(self.env["crm.lead"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1]).mapped(
            "expected_revenue"))
        week_revenue = round(sum(self.env["sale.order"].search([('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1]).mapped("amount_total")),
                             2)
        week_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_win_list = len([i.id for i in week_win_count])
        week_win_ratio = round((week_win_list / (week_lead_count + week_opp_count)) * 100, 2)

        week_win_manager = (self.env["crm.lead"]).search([('stage_id.is_won', '=', True)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_win_manager_count = len([i.id for i in week_win_manager])
        week_loss_manager = (self.env["crm.lead"]).search(
            [('active', '=', False)]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_loss_manager_count = len([i.id for i in week_loss_manager])

        rec.update({
            "week_lead_count": week_lead_count,
            "week_opp_count": week_opp_count,
            "week_expected_revenue": week_expected_revenue,
            "week_revenue": week_revenue,
            "week_win_ratio": week_win_ratio,
            "week_win_manager_count": week_win_manager_count,
            "week_loss_manager_count": week_loss_manager_count

        })
        return rec

    @api.model
    def crm_quarter(self):
        start_date, end_date = date_utils.get_quarter(fields.Date.today())
        rec = {}
        quarter_lead_count = self.env["crm.lead"].search_count(
            [('type', '=', 'lead'), ('user_id', '=', self.env.user.id), ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        quarter_opp_count = self.env["crm.lead"].search_count(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id), ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        quarter_expected_revenue = sum(
            self.env["crm.lead"].search([('user_id', '=', self.env.user.id), ('create_date', '>=', start_date),
                                         ('create_date', '<=', end_date)]).mapped("expected_revenue"))

        quarter_revenue = round(
            sum(self.env["sale.order"].search([('user_id', '=', self.env.user.id), ('create_date', '>=', start_date),
                                               ('create_date', '<=', end_date)]).mapped("amount_total")),
            2)

        quarter_win_count = (self.env["crm.lead"]).search_count(
            [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id), ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])
        quarter_win_ratio = round((quarter_win_count / (quarter_lead_count + quarter_opp_count)) * 100, 2)

        quarter_win_manager_count = (self.env["crm.lead"]).search_count(
            [('stage_id.is_won', '=', True), ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        quarter_loss_manager_count = (self.env["crm.lead"]).search_count(
            [('active', '=', False), ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        rec.update({
            "quarter_lead_count": quarter_lead_count,
            "quarter_opp_count": quarter_opp_count,
            "quarter_expected_revenue": quarter_expected_revenue,
            "quarter_revenue": quarter_revenue,
            "quarter_win_ratio": quarter_win_ratio,
            "quarter_win_manager_count": quarter_win_manager_count,
            "quarter_loss_manager_count": quarter_loss_manager_count
        })

        return rec

    @api.model
    def get_year_crm_activity(self):
        mail = self.env["mail.activity"].search([('res_model', '=', 'crm.lead')]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year)
        mail_type_list = [re.activity_type_id.id for re in mail]
        year_crm_activity = {rec.name: mail_type_list.count(rec.id) for rec in mail.activity_type_id}

        return year_crm_activity

    @api.model
    def get_month_crm_activity(self):
        mail = self.env["mail.activity"].search([('res_model', '=', 'crm.lead')]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        mail_type_list = [re.activity_type_id.id for re in mail]
        month_crm_activity = {rec.name: mail_type_list.count(rec.id) for rec in mail.activity_type_id}

        return month_crm_activity

    @api.model
    def get_week_crm_activity(self):
        mail = self.env["mail.activity"].search([('res_model', '=', 'crm.lead')]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        mail_type_list = [re.activity_type_id.id for re in mail]
        week_crm_activity = {rec.name: mail_type_list.count(rec.id) for rec in mail.activity_type_id}

        return week_crm_activity
    @api.model
    def get_quarter_crm_activity(self):
        start_date, end_date = date_utils.get_quarter(fields.Date.today())
        mail = self.env["mail.activity"].search([('res_model', '=', 'crm.lead'), ('create_date', '>=', start_date),
                                                 ('create_date', '<=', end_date)])
        mail_type_list = [re.activity_type_id.id for re in mail]
        quarter_crm_activity = {rec.name: mail_type_list.count(rec.id) for rec in mail.activity_type_id}

        return quarter_crm_activity
